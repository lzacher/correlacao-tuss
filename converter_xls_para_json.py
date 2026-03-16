#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor XLS → JSON — Correlação TUSS
=======================================
Converte o arquivo Excel da ANS para JSON sem modificar o aplicativo HTML.

O HTML (CorrelacaoTUSS_Interativa_v2.html) carrega o JSON dinamicamente,
portanto basta substituir o arquivo JSON para atualizar os dados.

Uso:
  python converter_xls_para_json.py --arquivo novo_tuss.xlsx
  python converter_xls_para_json.py --arquivo novo_tuss.xlsx --versao 2026.01
  python converter_xls_para_json.py --arquivo novo_tuss.xlsx --sem-push
  python converter_xls_para_json.py --verificar
"""

import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    print("Dependencia ausente: pandas\nExecute: pip install pandas openpyxl")
    sys.exit(1)

REPO_DIR  = Path(__file__).parent.resolve()
JSON_FILE = REPO_DIR / "CorrelacaoTUSS_2025.json"
LOG_FILE  = REPO_DIR / "atualizacoes.log"


# ─── Logger ───────────────────────────────────────────────────────────────────

class Logger:
    def __init__(self, path):
        self.path = path
        self._ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _w(self, nivel, msg):
        linha = f"[{datetime.now().strftime('%H:%M:%S')}] [{nivel}] {msg}"
        print(linha)
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(f"[{self._ts}] {linha}\n")

    def info(self, m):  self._w("INFO ", m)
    def ok(self, m):    self._w("OK   ", f"✓ {m}")
    def warn(self, m):  self._w("AVISO", f"⚠ {m}")
    def erro(self, m):  self._w("ERRO ", f"✗ {m}")
    def step(self, n, t, m): self._w("PASSO", f"[{n}/{t}] {m}")


log = Logger(LOG_FILE)


# ─── Conversão XLS → JSON ─────────────────────────────────────────────────────

def converter(caminho: Path, versao: str) -> dict | None:
    log.info(f"Lendo: {caminho.name}")
    try:
        xls    = pd.ExcelFile(caminho)
        aba    = xls.sheet_names[0]
        log.info(f"Aba: '{aba}'")

        df = pd.read_excel(caminho, sheet_name=aba, header=None)

        # Localizar linha de cabeçalho
        header_row = None
        for i, row in df.iterrows():
            if any("digo" in str(v) for v in row.values):
                header_row = i
                break
        if header_row is None:
            log.erro("Cabeçalho não encontrado.")
            return None

        df = pd.read_excel(caminho, sheet_name=aba, header=header_row)
        df = df.dropna(how="all").reset_index(drop=True)

        # Normalizar datas e NaN
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%d/%m/%Y")
        df = df.where(pd.notnull(df), None)

        registros = df.to_dict(orient="records")
        total     = len(registros)

        col_corr = next(
            (c for c in df.columns if "Sim" in str(c) or "Não" in str(c) or "orrel" in str(c)),
            None,
        )
        sim = sum(1 for r in registros if str(r.get(col_corr, "")).upper() == "SIM") if col_corr else 0

        dados = {
            "metadata": {
                "titulo":            "Correlação TUSS - Rol RN 465/2021",
                "descricao":         "Correlação entre Terminologia TUSS e Rol de Procedimentos ANS.",
                "versao":            versao,
                "data_atualizacao":  datetime.now().strftime("%d/%m/%Y"),
                "fonte":             "ANS - Agência Nacional de Saúde Suplementar",
                "total_registros":   total,
                "com_correlacao":    sim,
                "sem_correlacao":    total - sim,
            },
            "data": registros,
        }

        log.ok(f"Convertido: {total} registros ({sim} SIM / {total - sim} NÃO)")
        return dados

    except Exception as e:
        log.erro(f"Falha na conversão: {e}")
        return None


def salvar_json(dados: dict, versao: str) -> Path | None:
    """Salva o JSON e retorna o caminho do arquivo criado."""
    try:
        def serial(obj):
            if hasattr(obj, "strftime"):
                return obj.strftime("%d/%m/%Y")
            return str(obj)

        # Salvar com nome versionado
        nome_versionado = REPO_DIR / f"CorrelacaoTUSS_{versao}.json"
        with open(nome_versionado, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2, default=serial)

        # Manter também o nome padrão (compatibilidade com HTML)
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2, default=serial)

        tam = nome_versionado.stat().st_size / 1024 / 1024
        log.ok(f"JSON salvo: {nome_versionado.name} ({tam:.1f} MB)")
        log.ok(f"JSON padrão atualizado: {JSON_FILE.name}")
        return nome_versionado

    except Exception as e:
        log.erro(f"Falha ao salvar JSON: {e}")
        return None


def git_push(versao: str, total: int) -> bool:
    """Faz commit e push apenas do JSON atualizado."""
    msg = (
        f"chore: Atualiza dados TUSS v{versao}\n\n"
        f"- Total de registros: {total}\n"
        f"- Data: {datetime.now().strftime('%d/%m/%Y')}\n"
        f"- Apenas o JSON foi atualizado (HTML inalterado)"
    )
    for cmd, desc in [
        (["git", "add", "*.json"],             "Staging JSON"),
        (["git", "commit", "-m", msg],          "Commit"),
        (["git", "push", "origin", "HEAD"],     "Push"),
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_DIR)
        if r.returncode != 0:
            log.erro(f"{desc}: {r.stderr.strip()}")
            return False
        log.ok(desc)
    return True


def verificar():
    print("\n" + "=" * 60)
    print("  VERIFICAÇÃO DO REPOSITÓRIO")
    print("=" * 60 + "\n")

    arquivos = {
        "Aplicativo HTML (v2)": REPO_DIR / "CorrelacaoTUSS_Interativa_v2.html",
        "Aplicativo HTML (v1)": REPO_DIR / "CorrelacaoTUSS_Interativa.html",
        "Dados JSON (padrão)":  JSON_FILE,
        "Conversor XLS→JSON":   REPO_DIR / "converter_xls_para_json.py",
        "Atualizador completo": REPO_DIR / "atualizar_tuss.py",
    }

    for nome, caminho in arquivos.items():
        if caminho.exists():
            tam = caminho.stat().st_size / 1024
            print(f"  ✓ {nome:<30} {tam:>8.1f} KB")
        else:
            print(f"  ✗ {nome:<30} AUSENTE")

    if JSON_FILE.exists():
        try:
            with open(JSON_FILE, encoding="utf-8") as f:
                dados = json.load(f)
            meta = dados.get("metadata", {})
            print(f"\n  Dados JSON atuais:")
            print(f"    Versão:          {meta.get('versao', 'N/A')}")
            print(f"    Atualizado em:   {meta.get('data_atualizacao', 'N/A')}")
            print(f"    Total:           {meta.get('total_registros', 'N/A')} registros")
            print(f"    Com correlação:  {meta.get('com_correlacao', 'N/A')}")
        except Exception as e:
            print(f"\n  Erro ao ler JSON: {e}")

    r = subprocess.run(["git", "log", "--oneline", "-3"], capture_output=True, text=True, cwd=REPO_DIR)
    if r.returncode == 0:
        print(f"\n  Últimos commits:")
        for l in r.stdout.strip().split("\n"):
            print(f"    {l}")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Converte XLS da ANS para JSON sem modificar o HTML.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--arquivo", "-a", type=Path, help="Arquivo Excel (.xlsx) da ANS")
    parser.add_argument("--versao",  "-v", default=datetime.now().strftime("%Y.%m"),
                        help="Versão dos dados (padrão: AAAA.MM)")
    parser.add_argument("--sem-push", action="store_true",
                        help="Não faz push para o GitHub")
    parser.add_argument("--verificar", action="store_true",
                        help="Verifica o estado atual do repositório")
    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  CONVERSOR XLS → JSON — CORRELAÇÃO TUSS")
    print("=" * 60 + "\n")

    if args.verificar:
        verificar()
        return

    if not args.arquivo:
        parser.print_help()
        print("\nInforme o arquivo Excel com --arquivo caminho/para/arquivo.xlsx\n")
        sys.exit(1)

    if not args.arquivo.exists():
        log.erro(f"Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)

    total_etapas = 2 if args.sem_push else 3

    # Etapa 1: Converter
    log.step(1, total_etapas, "Convertendo XLS para JSON...")
    dados = converter(args.arquivo, args.versao)
    if not dados:
        sys.exit(1)

    # Etapa 2: Salvar
    log.step(2, total_etapas, "Salvando JSON...")
    json_path = salvar_json(dados, args.versao)
    if not json_path:
        sys.exit(1)

    # Etapa 3: Push
    if not args.sem_push:
        log.step(3, total_etapas, "Enviando JSON para o GitHub...")
        if not git_push(args.versao, dados["metadata"]["total_registros"]):
            log.warn("Push falhou. Faça manualmente: git add *.json && git commit -m 'chore: atualiza JSON' && git push")
        else:
            log.ok("JSON publicado no GitHub!")

    print("\n" + "=" * 60)
    print("  CONVERSÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"\n  Versão:    {args.versao}")
    print(f"  Registros: {dados['metadata']['total_registros']}")
    print(f"  JSON:      {json_path.name}")
    print(f"\n  Para atualizar o aplicativo HTML:")
    print(f"  1. Copie o arquivo '{json_path.name}' para a pasta do HTML")
    print(f"  2. Abra o HTML no navegador")
    print(f"  3. Use a barra amarela para carregar o novo JSON")
    print(f"  4. Os dados são atualizados sem reinstalar nada!\n")


if __name__ == "__main__":
    main()
