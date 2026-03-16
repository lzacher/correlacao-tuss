#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
converter_xls_para_json.py
==========================
Utilitário para manter a tabela de Correlação TUSS atualizada.

Fluxo completo (modo padrão - sem argumentos):
  1. Acessa a página da ANS e detecta o arquivo XLSX mais recente
  2. Baixa o arquivo automaticamente (simulando navegador para evitar bloqueio 403)
  3. Converte para JSON estruturado
  4. Salva como CorrelacaoTUSS_dados.json (nome fixo, lido pelo HTML automaticamente)
  5. Salva cópia versionada (ex: CorrelacaoTUSS_2025.03.json)
  6. Exibe resumo completo

Modos de uso:
  python converter_xls_para_json.py                    # Download automático da ANS
  python converter_xls_para_json.py --arquivo meu.xlsx # Usar arquivo local
  python converter_xls_para_json.py --verificar        # Checar versão disponível na ANS
  python converter_xls_para_json.py --push             # Converter + push ao GitHub
  python converter_xls_para_json.py --saida /pasta     # Definir pasta de saída

Requisitos:
  pip install requests beautifulsoup4 pandas openpyxl
"""

import os
import sys
import json
import argparse
import tempfile
import subprocess
import re
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERRO] Instale: pip install requests beautifulsoup4")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("[ERRO] Instale: pip install pandas openpyxl")
    sys.exit(1)

# ─── Configurações ─────────────────────────────────────────────────────────────

ANS_PAGINA = (
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/"
    "participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
)
ANS_BASE_URL = "https://www.gov.br"

# Nome fixo do JSON principal — é este que o HTML carrega automaticamente
JSON_PRINCIPAL = "CorrelacaoTUSS_dados.json"

REPO_DIR = Path(__file__).parent.resolve()
LOG_FILE = REPO_DIR / "atualizacoes.log"

# Headers que simulam navegador Chrome real (necessário para evitar bloqueio 403 da ANS)
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": ANS_PAGINA,
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


# ─── Logger ────────────────────────────────────────────────────────────────────

def log(nivel, msg):
    icones = {"OK": "✓", "ERRO": "✗", "INFO": "→", "PASSO": "◆", "AVISO": "⚠"}
    icone = icones.get(nivel, "·")
    linha = f"[{nivel:<5}] {icone} {msg}"
    print(linha)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{ts}] {linha}\n")
    except Exception:
        pass


# ─── Detecção do arquivo mais recente na ANS ──────────────────────────────────

def detectar_arquivo_ans():
    """
    Acessa a página da ANS e retorna (nome_arquivo, url_download) do
    arquivo de Correlação TUSS mais recente publicado.
    """
    log("PASSO", "Consultando página da ANS para detectar versão mais recente...")
    try:
        r = requests.get(ANS_PAGINA, headers=HEADERS, timeout=30)
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Não foi possível acessar a página da ANS: {e}")

    soup = BeautifulSoup(r.text, "html.parser")
    candidatos = []

    for a in soup.find_all("a", href=True):
        href = a["href"]
        nome = os.path.basename(href.split("?")[0]).rstrip("/")
        nome_lower = nome.lower()

        # Critério: arquivo de correlação TUSS em XLS/XLSX
        if (("correlac" in nome_lower or "correla" in nome_lower)
                and "tuss" in nome_lower
                and (nome_lower.endswith(".xlsx") or nome_lower.endswith(".xls"))):

            # Montar URL de download direto (padrão Plone CMS da ANS: @@download/file)
            base = href.rstrip("/").replace("/view", "").replace("/@@download/file", "")
            url_dl = (base if base.startswith("http") else ANS_BASE_URL + base) + "/@@download/file"
            candidatos.append((nome, url_dl))

    if not candidatos:
        raise RuntimeError(
            "Nenhum arquivo de Correlação TUSS encontrado na página da ANS.\n"
            f"Verifique manualmente: {ANS_PAGINA}"
        )

    # Remover duplicatas e ordenar pelo nome (mais recente = maior string)
    vistos = set()
    unicos = []
    for item in candidatos:
        if item[0] not in vistos:
            vistos.add(item[0])
            unicos.append(item)
    unicos.sort(key=lambda x: x[0], reverse=True)

    nome_escolhido, url_escolhida = unicos[0]
    log("OK",   f"Arquivo mais recente: {nome_escolhido}")
    log("INFO", f"URL de download: {url_escolhida}")

    if len(unicos) > 1:
        log("INFO", f"Outros arquivos disponíveis ({len(unicos) - 1}):")
        for nome, _ in unicos[1:4]:
            log("INFO", f"  · {nome}")

    return nome_escolhido, url_escolhida


# ─── Download ─────────────────────────────────────────────────────────────────

def baixar_arquivo(url, destino):
    """Baixa o arquivo XLSX da ANS simulando um navegador real."""
    log("PASSO", "Baixando arquivo da ANS...")
    try:
        r = requests.get(url, headers=HEADERS, stream=True, timeout=60)
        r.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Falha no download: {e}")

    content_type = r.headers.get("Content-Type", "")
    if "html" in content_type:
        raise RuntimeError(
            "O servidor retornou HTML em vez do arquivo XLSX. "
            "Possível bloqueio anti-bot ou URL incorreta."
        )

    with open(destino, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    tamanho = os.path.getsize(destino) / 1024
    log("OK", f"Download concluído: {tamanho:.1f} KB")


# ─── Conversão XLSX → JSON ────────────────────────────────────────────────────

def converter(caminho_xlsx, nome_arquivo=""):
    """Lê o XLSX e retorna (dados_dict, versao_str)."""
    log("PASSO", "Convertendo XLSX para JSON...")

    # Abrir com openpyxl (xlsx) ou xlrd (xls legado)
    try:
        xl = pd.ExcelFile(str(caminho_xlsx), engine="openpyxl")
    except Exception:
        try:
            xl = pd.ExcelFile(str(caminho_xlsx), engine="xlrd")
        except Exception as e:
            raise RuntimeError(f"Não foi possível abrir o arquivo Excel: {e}")

    # Detectar aba correta
    aba = xl.sheet_names[0]
    for nome_aba in xl.sheet_names:
        if any(k in nome_aba.lower() for k in ["correlac", "tuss", "rol", "procedimento"]):
            aba = nome_aba
            break
    log("INFO", f"Aba utilizada: \"{aba}\"")

    # Ler sem cabeçalho para detectar linha de cabeçalho
    df_raw = pd.read_excel(str(caminho_xlsx), sheet_name=aba,
                           header=None, engine="openpyxl", nrows=25)
    linha_header = 0
    for i, row in df_raw.iterrows():
        vals = [str(v).lower() for v in row if pd.notna(v)]
        if any("digo" in v or "código" in v or "codigo" in v for v in vals):
            linha_header = i
            break
    log("INFO", f"Cabeçalho na linha: {linha_header + 1}")

    # Ler com cabeçalho correto
    df = pd.read_excel(str(caminho_xlsx), sheet_name=aba,
                       header=linha_header, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(how="all").reset_index(drop=True)

    # Converter datas para string legível
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%d/%m/%Y")
    df = df.where(pd.notna(df), None)

    registros = df.to_dict(orient="records")
    total = len(registros)

    # Detectar coluna de correlação
    col_corr = None
    for col in df.columns:
        if "correla" in col.lower():
            col_corr = col
            break
    if not col_corr:
        for col in df.columns:
            vals = df[col].dropna().astype(str).str.upper().unique()
            if "SIM" in vals and any(v in vals for v in ["NÃO", "NAO", "NÂO"]):
                col_corr = col
                break

    sim = 0
    if col_corr:
        sim = int(df[col_corr].astype(str).str.upper().eq("SIM").sum())
    log("INFO", f"Correlação: coluna=\"{col_corr}\" | SIM={sim} | NÃO={total - sim}")

    # Extrair versão TUSS do nome do arquivo (ex: TUSS202503 → 2025.03)
    versao = datetime.now().strftime("%Y.%m")
    if nome_arquivo:
        m = re.search(r"TUSS(\d{4})(\d{2})", nome_arquivo, re.IGNORECASE)
        if m:
            versao = f"{m.group(1)}.{m.group(2)}"

    dados = {
        "metadata": {
            "titulo":            "Correlação TUSS — Rol de Procedimentos ANS",
            "descricao":         (
                "Correlação entre a Terminologia Unificada da Saúde Suplementar (TUSS) "
                "e o Rol de Procedimentos e Eventos em Saúde da ANS (RN 465/2021)."
            ),
            "versao":            versao,
            "data_atualizacao":  datetime.now().strftime("%d/%m/%Y %H:%M"),
            "fonte":             "ANS — Agência Nacional de Saúde Suplementar",
            "url_fonte":         ANS_PAGINA,
            "arquivo_origem":    nome_arquivo or os.path.basename(str(caminho_xlsx)),
            "total_registros":   total,
            "com_correlacao":    sim,
            "sem_correlacao":    total - sim,
            "coluna_correlacao": col_corr or "não detectada",
        },
        "data": registros,
    }

    log("OK", f"Conversão concluída: {total:,} registros ({sim:,} SIM / {total - sim:,} NÃO)")
    return dados, versao


# ─── Salvar JSON ──────────────────────────────────────────────────────────────

def salvar_json(dados, diretorio, versao):
    """
    Salva dois arquivos JSON:
      1. CorrelacaoTUSS_dados.json  — nome FIXO, carregado automaticamente pelo HTML
      2. CorrelacaoTUSS_{versao}.json — cópia versionada para histórico
    """
    diretorio = Path(diretorio)
    diretorio.mkdir(parents=True, exist_ok=True)

    def serial(obj):
        if hasattr(obj, "strftime"):
            return obj.strftime("%d/%m/%Y")
        return str(obj)

    conteudo = json.dumps(dados, ensure_ascii=False, indent=2, default=serial)

    # 1. Arquivo principal (nome fixo — HTML carrega este automaticamente)
    p_principal = diretorio / JSON_PRINCIPAL
    p_principal.write_text(conteudo, encoding="utf-8")
    tam = p_principal.stat().st_size / 1024 / 1024
    log("OK", f"JSON principal: {p_principal.name} ({tam:.1f} MB)")

    # 2. Cópia versionada para histórico
    p_versao = diretorio / f"CorrelacaoTUSS_{versao}.json"
    p_versao.write_text(conteudo, encoding="utf-8")
    log("OK", f"JSON versionado: {p_versao.name}")

    return p_principal, p_versao


# ─── Push GitHub ──────────────────────────────────────────────────────────────

def push_github(diretorio, versao, total):
    """Faz commit e push dos arquivos JSON atualizados para o GitHub."""
    log("PASSO", "Fazendo commit e push para o GitHub...")
    msg = (
        f"chore: Atualiza dados TUSS v{versao} via download automatico ANS\n\n"
        f"- Total: {total:,} registros\n"
        f"- Data: {datetime.now().strftime('%d/%m/%Y')}\n"
        f"- HTML inalterado (apenas JSON atualizado)"
    )
    cmds = [
        (["git", "add", JSON_PRINCIPAL, f"CorrelacaoTUSS_{versao}.json"], "Staging"),
        (["git", "commit", "-m", msg], "Commit"),
        (["git", "push", "origin", "HEAD"], "Push"),
    ]
    for cmd, desc in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(diretorio))
        if r.returncode != 0:
            log("AVISO", f"{desc} falhou: {r.stderr.strip()}")
            return False
        log("OK", desc)
    return True


# ─── Verificar versão na ANS ──────────────────────────────────────────────────

def verificar_versao():
    """Apenas verifica qual versão está disponível na ANS sem baixar."""
    print("\n" + "=" * 60)
    print("  VERIFICAÇÃO — VERSÃO DISPONÍVEL NA ANS")
    print("=" * 60)
    try:
        nome, url = detectar_arquivo_ans()
        print(f"\n  Arquivo mais recente : {nome}")
        print(f"  URL de download      : {url}")
        print(f"\n  Página da ANS        : {ANS_PAGINA}")
    except RuntimeError as e:
        log("ERRO", str(e))
        sys.exit(1)

    # Comparar com JSON local
    p_local = REPO_DIR / JSON_PRINCIPAL
    if p_local.exists():
        try:
            with open(p_local, encoding="utf-8") as f:
                meta = json.load(f).get("metadata", {})
            print(f"\n  Versão local atual   : {meta.get('versao', 'N/A')}")
            print(f"  Atualizado em        : {meta.get('data_atualizacao', 'N/A')}")
            print(f"  Registros            : {meta.get('total_registros', 'N/A')}")
        except Exception:
            pass
    print("=" * 60 + "\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Atualiza a tabela de Correlação TUSS a partir da ANS.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--arquivo", "-a",
                        help="Arquivo XLS/XLSX local (ignora download automático da ANS)")
    parser.add_argument("--saida", "-s", default=str(REPO_DIR),
                        help="Pasta de saída dos arquivos JSON (padrão: pasta do script)")
    parser.add_argument("--verificar", "-v", action="store_true",
                        help="Apenas verifica a versão disponível na ANS sem baixar")
    parser.add_argument("--push", "-p", action="store_true",
                        help="Após converter, faz commit e push para o GitHub")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  CORRELAÇÃO TUSS — CONVERSOR E ATUALIZADOR AUTOMÁTICO")
    print("=" * 60 + "\n")

    if args.verificar:
        verificar_versao()
        return

    nome_arquivo = ""
    caminho_xlsx = None
    tmp_criado = False

    try:
        if args.arquivo:
            # Modo local: usar arquivo fornecido pelo usuário
            caminho_xlsx = Path(args.arquivo)
            if not caminho_xlsx.exists():
                log("ERRO", f"Arquivo não encontrado: {caminho_xlsx}")
                sys.exit(1)
            nome_arquivo = caminho_xlsx.name
            log("INFO", f"Usando arquivo local: {nome_arquivo}")
        else:
            # Modo automático: detectar e baixar da ANS
            nome_arquivo, url_download = detectar_arquivo_ans()
            sufixo = ".xlsx" if nome_arquivo.lower().endswith(".xlsx") else ".xls"
            tmp = tempfile.NamedTemporaryFile(suffix=sufixo, delete=False)
            tmp.close()
            caminho_xlsx = Path(tmp.name)
            tmp_criado = True
            baixar_arquivo(url_download, caminho_xlsx)

        # Converter XLSX → JSON
        dados, versao = converter(caminho_xlsx, nome_arquivo)

        # Salvar arquivos JSON
        p_principal, p_versao = salvar_json(dados, args.saida, versao)

        # Push opcional para o GitHub
        if args.push:
            push_github(Path(args.saida), versao, dados["metadata"]["total_registros"])

        # Resumo final
        meta = dados["metadata"]
        print("\n" + "=" * 60)
        print("  ATUALIZAÇÃO CONCLUÍDA COM SUCESSO")
        print("=" * 60)
        print(f"  Versão TUSS     : {meta['versao']}")
        print(f"  Atualizado em   : {meta['data_atualizacao']}")
        print(f"  Total registros : {meta['total_registros']:,}")
        print(f"  Com correlação  : {meta['com_correlacao']:,} (SIM)")
        print(f"  Sem correlação  : {meta['sem_correlacao']:,} (NÃO)")
        print(f"  Arquivo origem  : {meta['arquivo_origem']}")
        print(f"\n  JSON principal  : {p_principal}")
        print(f"  JSON versionado : {p_versao}")
        print(f"\n  O HTML carregará automaticamente: {JSON_PRINCIPAL}")
        print("=" * 60 + "\n")

    except RuntimeError as e:
        log("ERRO", str(e))
        sys.exit(1)
    finally:
        # Limpar arquivo temporário
        if tmp_criado and caminho_xlsx and caminho_xlsx.exists():
            try:
                caminho_xlsx.unlink()
            except Exception:
                pass


if __name__ == "__main__":
    main()
