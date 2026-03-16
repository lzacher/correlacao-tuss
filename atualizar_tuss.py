#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Atualização Automática - Correlação TUSS
===================================================
Automatiza o processo de atualização dos dados TUSS no repositório GitHub.

Fluxo:
  1. Recebe o novo arquivo Excel (.xlsx) da ANS
  2. Converte para JSON estruturado
  3. Regenera a tabela HTML interativa
  4. Recria o pacote ZIP de distribuição
  5. Faz commit e push para o GitHub

Uso:
  python atualizar_tuss.py --arquivo novo_tuss.xlsx
  python atualizar_tuss.py --arquivo novo_tuss.xlsx --versao 2026.01
  python atualizar_tuss.py --arquivo novo_tuss.xlsx --sem-push
  python atualizar_tuss.py --verificar
"""

import os
import sys
import json
import shutil
import zipfile
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# ─── Dependências opcionais ───────────────────────────────────────────────────
try:
    import pandas as pd
except ImportError:
    print("❌ Dependência ausente: pandas\n   Execute: pip install pandas openpyxl")
    sys.exit(1)

# ─── Configurações ────────────────────────────────────────────────────────────
REPO_DIR        = Path(__file__).parent.resolve()
HTML_FILE       = REPO_DIR / "CorrelacaoTUSS_Interativa.html"
JSON_FILE       = REPO_DIR / "CorrelacaoTUSS_2025.json"
ZIP_FILE        = REPO_DIR / "Correlacao_TUSS_v1.0.zip"
LOG_FILE        = REPO_DIR / "atualizacoes.log"

# Colunas esperadas no Excel da ANS
COLUNAS_ESPERADAS = [
    "Código",
    "Terminologia de Procedimentos e Eventos em Saúde",
    "Correlação\n(Sim/Não)",
    "PROCEDIMENTO",
]

# ─── Utilitários ──────────────────────────────────────────────────────────────

class Logger:
    """Registra mensagens no console e em arquivo de log."""

    def __init__(self, log_path: Path):
        self.log_path = log_path
        self._session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _write(self, nivel: str, msg: str):
        linha = f"[{datetime.now().strftime('%H:%M:%S')}] [{nivel}] {msg}"
        print(linha)
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"[{self._session}] {linha}\n")

    def info(self, msg):    self._write("INFO ", msg)
    def ok(self, msg):      self._write("OK   ", f"✓ {msg}")
    def warn(self, msg):    self._write("AVISO", f"⚠ {msg}")
    def erro(self, msg):    self._write("ERRO ", f"✗ {msg}")
    def step(self, n, total, msg): self._write("PASSO", f"[{n}/{total}] {msg}")


log = Logger(LOG_FILE)


def executar(cmd: list, descricao: str) -> bool:
    """Executa um comando de shell e retorna True se bem-sucedido."""
    try:
        resultado = subprocess.run(
            cmd, capture_output=True, text=True, cwd=REPO_DIR
        )
        if resultado.returncode != 0:
            log.erro(f"{descricao}: {resultado.stderr.strip()}")
            return False
        return True
    except FileNotFoundError as e:
        log.erro(f"{descricao}: comando não encontrado — {e}")
        return False


# ─── Etapa 1: Converter Excel → JSON ─────────────────────────────────────────

def converter_excel_para_json(caminho_excel: Path, versao: str) -> dict | None:
    """Lê o Excel da ANS e retorna o dicionário JSON estruturado."""
    log.info(f"Lendo arquivo: {caminho_excel.name}")

    try:
        # Tentar detectar a aba correta
        xls = pd.ExcelFile(caminho_excel)
        aba = xls.sheet_names[0]
        log.info(f"Aba selecionada: '{aba}'")

        df = pd.read_excel(caminho_excel, sheet_name=aba, header=None)

        # Localizar a linha de cabeçalho (contém "Código")
        header_row = None
        for i, row in df.iterrows():
            if any("digo" in str(v) for v in row.values):
                header_row = i
                break

        if header_row is None:
            log.erro("Cabeçalho não encontrado no arquivo Excel.")
            return None

        df = pd.read_excel(caminho_excel, sheet_name=aba, header=header_row)
        df = df.dropna(how="all").reset_index(drop=True)

        # Converter datas para string
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime("%d/%m/%Y")

        # Substituir NaN por None
        df = df.where(pd.notnull(df), None)

        registros = df.to_dict(orient="records")
        total = len(registros)

        # Contar correlações
        col_corr = next(
            (c for c in df.columns if "Sim" in str(c) or "Não" in str(c) or "orrel" in str(c)),
            None,
        )
        sim = sum(1 for r in registros if str(r.get(col_corr, "")).upper() == "SIM") if col_corr else 0
        nao = total - sim

        dados = {
            "metadata": {
                "titulo": "Correlação TUSS - Rol RN 465/2021",
                "descricao": (
                    "Tabela de Correlação entre Terminologia de Procedimentos e Eventos "
                    "em Saúde e o Rol de Procedimentos e Eventos em Saúde RN nº 465/2021."
                ),
                "versao": versao,
                "data_atualizacao": datetime.now().strftime("%d/%m/%Y"),
                "fonte": "ANS - Agência Nacional de Saúde Suplementar",
                "total_registros": total,
                "com_correlacao": sim,
                "sem_correlacao": nao,
            },
            "colunas": {str(c): str(c) for c in df.columns},
            "data": registros,
        }

        log.ok(f"Conversão concluída: {total} registros ({sim} SIM / {nao} NÃO)")
        return dados

    except Exception as e:
        log.erro(f"Falha na conversão: {e}")
        return None


# ─── Etapa 2: Salvar JSON ─────────────────────────────────────────────────────

def salvar_json(dados: dict) -> bool:
    """Salva o dicionário como JSON no repositório."""
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
        tamanho = JSON_FILE.stat().st_size / 1024 / 1024
        log.ok(f"JSON salvo: {JSON_FILE.name} ({tamanho:.1f} MB)")
        return True
    except Exception as e:
        log.erro(f"Falha ao salvar JSON: {e}")
        return False


# ─── Etapa 3: Regenerar HTML ──────────────────────────────────────────────────

def regenerar_html(dados: dict) -> bool:
    """Gera a tabela HTML interativa a partir dos dados atualizados."""
    try:
        meta     = dados["metadata"]
        registros = dados["data"]
        def serializar(obj):
            if hasattr(obj, 'isoformat'):
                return obj.strftime('%d/%m/%Y') if hasattr(obj, 'strftime') else str(obj)
            return str(obj)
        records_json = json.dumps(registros, ensure_ascii=False, default=serializar)

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Correlação TUSS - Visualização Interativa</title>
    <style>
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:20px}}
        .container{{max-width:1400px;margin:0 auto;background:#fff;border-radius:12px;box-shadow:0 20px 60px rgba(0,0,0,.3);overflow:hidden}}
        .header{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;padding:30px;text-align:center}}
        .header h1{{font-size:28px;margin-bottom:10px}}
        .header p{{font-size:14px;opacity:.9;margin-bottom:5px}}
        .info-bar{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;padding:20px 30px;background:#f8f9fa;border-bottom:1px solid #e0e0e0}}
        .info-item{{display:flex;flex-direction:column}}
        .info-label{{font-size:12px;color:#666;font-weight:600;text-transform:uppercase;margin-bottom:5px}}
        .info-value{{font-size:16px;color:#333;font-weight:500}}
        .controls{{padding:20px 30px;background:#fff;border-bottom:1px solid #e0e0e0;display:flex;gap:15px;flex-wrap:wrap;align-items:center}}
        .search-box{{flex:1;min-width:250px;display:flex;gap:10px;align-items:center}}
        .search-box input{{flex:1;padding:10px 15px;border:2px solid #e0e0e0;border-radius:6px;font-size:14px;transition:border-color .3s}}
        .search-box input:focus{{outline:none;border-color:#667eea}}
        .clear-btn{{padding:10px 15px;border:2px solid #e0e0e0;background:#fff;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;color:#666;transition:all .3s;white-space:nowrap}}
        .clear-btn:hover{{border-color:#dc3545;color:#dc3545;background:#fff5f5}}
        .clear-btn:active{{transform:scale(.98)}}
        .filter-group{{display:flex;gap:10px;flex-wrap:wrap}}
        .filter-btn{{padding:8px 15px;border:2px solid #e0e0e0;background:#fff;border-radius:6px;cursor:pointer;font-size:13px;font-weight:500;transition:all .3s}}
        .filter-btn:hover{{border-color:#667eea;color:#667eea}}
        .filter-btn.active{{background:#667eea;color:#fff;border-color:#667eea}}
        .table-wrapper{{overflow-x:auto;padding:20px 30px;max-height:600px;overflow-y:auto}}
        table{{width:100%;border-collapse:collapse;font-size:13px}}
        thead{{background:#f8f9fa;position:sticky;top:0;z-index:10}}
        th{{padding:12px;text-align:left;font-weight:600;color:#333;border-bottom:2px solid #e0e0e0;cursor:pointer;user-select:none;white-space:nowrap;transition:background .3s}}
        th:hover{{background:#e8eaf6}}
        th.sortable::after{{content:' ⇅';opacity:.5;font-size:11px}}
        th.sorted-asc::after{{content:' ↑';opacity:1;color:#667eea}}
        th.sorted-desc::after{{content:' ↓';opacity:1;color:#667eea}}
        td{{padding:12px;border-bottom:1px solid #f0f0f0;color:#555}}
        tbody tr:hover{{background:#f8f9fa}}
        .badge{{display:inline-block;padding:4px 8px;border-radius:4px;font-size:11px;font-weight:600;text-transform:uppercase}}
        .badge-sim{{background:#d4edda;color:#155724}}
        .badge-nao{{background:#f8d7da;color:#721c24}}
        .coverage-badge{{display:inline-block;padding:3px 6px;margin:2px;border-radius:3px;background:#e3f2fd;color:#1565c0;font-size:10px;font-weight:600}}
        .stats{{padding:20px 30px;background:#f8f9fa;border-top:1px solid #e0e0e0;display:flex;gap:20px;flex-wrap:wrap;font-size:13px;color:#666}}
        .no-results{{text-align:center;padding:40px;color:#999}}
        .version-badge{{display:inline-block;background:rgba(255,255,255,.2);padding:4px 10px;border-radius:20px;font-size:12px;margin-top:8px}}
        @media(max-width:768px){{
            .header h1{{font-size:20px}}
            .controls{{flex-direction:column;align-items:stretch}}
            .search-box{{flex-direction:column}}
            .search-box input,.clear-btn{{width:100%}}
            table{{font-size:12px}}
            td,th{{padding:8px}}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📋 Correlação TUSS - Rol RN 465/2021</h1>
        <p>Tabela de Correlação entre Terminologia de Procedimentos e Eventos em Saúde</p>
        <p style="font-size:12px;margin-top:10px;opacity:.8">
            Atualizado em {meta['data_atualizacao']} | ANS - Agência Nacional de Saúde Suplementar
        </p>
        <span class="version-badge">v{meta['versao']}</span>
    </div>

    <div class="info-bar">
        <div class="info-item"><span class="info-label">Total de Registros</span><span class="info-value" id="total-records">{meta['total_registros']}</span></div>
        <div class="info-item"><span class="info-label">Com Correlação</span><span class="info-value" id="sim-count">-</span></div>
        <div class="info-item"><span class="info-label">Sem Correlação</span><span class="info-value" id="nao-count">-</span></div>
        <div class="info-item"><span class="info-label">Registros Exibidos</span><span class="info-value" id="displayed-count">{meta['total_registros']}</span></div>
    </div>

    <div class="controls">
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 Buscar por código, procedimento, terminologia...">
            <button class="clear-btn" id="clearBtn" title="Limpar pesquisa">✕ Limpar</button>
        </div>
        <div class="filter-group">
            <button class="filter-btn active" data-filter="all">Todos</button>
            <button class="filter-btn" data-filter="SIM">Com Correlação</button>
            <button class="filter-btn" data-filter="NÃO">Sem Correlação</button>
        </div>
    </div>

    <div class="table-wrapper">
        <table id="dataTable">
            <thead>
                <tr>
                    <th class="sortable" data-column="Código">Código</th>
                    <th class="sortable" data-column="Terminologia de Procedimentos e Eventos em Saúde (Tab. 22.202501)">Terminologia TUSS</th>
                    <th class="sortable" data-column="Correlação\\n(Sim/Não)">Correlação</th>
                    <th class="sortable" data-column="PROCEDIMENTO">Procedimento</th>
                    <th class="sortable" data-column="SUBGRUPO">Subgrupo</th>
                    <th class="sortable" data-column="GRUPO">Grupo</th>
                    <th class="sortable" data-column="CAPÍTULO">Capítulo</th>
                    <th>Cobertura</th>
                </tr>
            </thead>
            <tbody id="tableBody"></tbody>
        </table>
        <div id="noResults" class="no-results" style="display:none">Nenhum resultado encontrado para sua busca.</div>
    </div>

    <div class="stats">
        <span>💡 Dica: Clique nos cabeçalhos das colunas para ordenar os dados</span>
        <span id="filter-info"></span>
    </div>
</div>

<script>
const allRecords = {records_json};
let filteredRecords=[...allRecords],currentFilter='all',sortColumn=null,sortDirection='asc';
const searchInput=document.getElementById('searchInput');
const clearBtn=document.getElementById('clearBtn');
const filterButtons=document.querySelectorAll('.filter-btn');
const tableBody=document.getElementById('tableBody');
const noResults=document.getElementById('noResults');
const displayedCount=document.getElementById('displayed-count');
const simCount=document.getElementById('sim-count');
const naoCount=document.getElementById('nao-count');
const filterInfo=document.getElementById('filter-info');
const headers=document.querySelectorAll('th.sortable');

function updateStats(){{
    const corrCol=Object.keys(allRecords[0]||{{}}).find(k=>k.includes('Sim')||k.includes('Não')||k.includes('orrel'))||'Correlação\\n(Sim/Não)';
    simCount.textContent=allRecords.filter(r=>String(r[corrCol]||'').toUpperCase()==='SIM').length;
    naoCount.textContent=allRecords.filter(r=>String(r[corrCol]||'').toUpperCase()==='NÃO').length;
}}

function renderTable(){{
    tableBody.innerHTML='';
    if(!filteredRecords.length){{noResults.style.display='block';displayedCount.textContent='0';return;}}
    noResults.style.display='none';
    displayedCount.textContent=filteredRecords.length;
    filteredRecords.forEach(record=>{{
        const row=document.createElement('tr');
        const coverage=[];
        ['OD','AMB','HCO','HSO','PAC','DUT'].forEach(c=>{{if(record[c]&&record[c]!=='---')coverage.push(c);}});
        const corrCol=Object.keys(record).find(k=>k.includes('Sim')||k.includes('Não')||k.includes('orrel'))||'Correlação\\n(Sim/Não)';
        const corr=record[corrCol]||'-';
        const badgeClass=corr==='SIM'?'badge-sim':'badge-nao';
        const termCol=Object.keys(record).find(k=>k.toLowerCase().includes('terminologia'))||'';
        const procCol=Object.keys(record).find(k=>k==='PROCEDIMENTO')||'PROCEDIMENTO';
        row.innerHTML=`
            <td><strong>${{record['Código']||'-'}}</strong></td>
            <td>${{record[termCol]||'-'}}</td>
            <td><span class="badge ${{badgeClass}}">${{corr}}</span></td>
            <td>${{record[procCol]||'-'}}</td>
            <td>${{record['SUBGRUPO']||'-'}}</td>
            <td>${{record['GRUPO']||'-'}}</td>
            <td>${{record['CAPÍTULO']||'-'}}</td>
            <td>${{coverage.length?coverage.map(c=>`<span class="coverage-badge">${{c}}</span>`).join(''):'-'}}</td>`;
        tableBody.appendChild(row);
    }});
}}

function search(){{
    const q=searchInput.value.toLowerCase();
    const corrCol=Object.keys(allRecords[0]||{{}}).find(k=>k.includes('Sim')||k.includes('Não')||k.includes('orrel'))||'Correlação\\n(Sim/Não)';
    filteredRecords=allRecords.filter(r=>{{
        const matchSearch=!q||Object.values(r).some(v=>String(v||'').toLowerCase().includes(q));
        const matchFilter=currentFilter==='all'||String(r[corrCol]||'').toUpperCase()===currentFilter;
        return matchSearch&&matchFilter;
    }});
    if(sortColumn){{
        filteredRecords.sort((a,b)=>{{
            let av=a[sortColumn]||'',bv=b[sortColumn]||'';
            if(!isNaN(av)&&!isNaN(bv)){{av=parseFloat(av);bv=parseFloat(bv);}}
            else{{av=String(av).toLowerCase();bv=String(bv).toLowerCase();}}
            return av<bv?(sortDirection==='asc'?-1:1):av>bv?(sortDirection==='asc'?1:-1):0;
        }});
    }}
    renderTable();
    filterInfo.textContent=filteredRecords.length<allRecords.length?`Mostrando ${{filteredRecords.length}} de ${{allRecords.length}} registros`:`Mostrando todos os ${{allRecords.length}} registros`;
}}

clearBtn.addEventListener('click',()=>{{searchInput.value='';searchInput.focus();search();}});
filterButtons.forEach(btn=>btn.addEventListener('click',()=>{{
    filterButtons.forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    currentFilter=btn.dataset.filter;
    search();
}}));
headers.forEach(h=>h.addEventListener('click',()=>{{
    headers.forEach(x=>x.classList.remove('sorted-asc','sorted-desc'));
    if(sortColumn===h.dataset.column)sortDirection=sortDirection==='asc'?'desc':'asc';
    else{{sortColumn=h.dataset.column;sortDirection='asc';}}
    h.classList.add(sortDirection==='asc'?'sorted-asc':'sorted-desc');
    search();
}}));
searchInput.addEventListener('input',search);
updateStats();
search();
</script>
</body>
</html>"""

        with open(HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html)

        tamanho = HTML_FILE.stat().st_size / 1024 / 1024
        log.ok(f"HTML regenerado: {HTML_FILE.name} ({tamanho:.1f} MB)")
        return True

    except Exception as e:
        log.erro(f"Falha ao regenerar HTML: {e}")
        return False


# ─── Etapa 4: Recriar ZIP ─────────────────────────────────────────────────────

def recriar_zip(versao: str) -> bool:
    """Recria o pacote ZIP de distribuição com os arquivos atualizados."""
    try:
        nome_zip = REPO_DIR / f"Correlacao_TUSS_{versao}.zip"

        arquivos = [
            HTML_FILE,
            JSON_FILE,
            REPO_DIR / "instalador_tuss.py",
            REPO_DIR / "instalar_tuss.sh",
            REPO_DIR / "compilar_exe.bat",
            REPO_DIR / "compilar_exe.sh",
            REPO_DIR / "README.md",
            REPO_DIR / "GUIA_INSTALACAO.md",
            REPO_DIR / "LEIA-ME_EXE.md",
        ]

        pasta_zip = f"Correlacao_TUSS_{versao}"

        with zipfile.ZipFile(nome_zip, "w", zipfile.ZIP_DEFLATED) as zf:
            for arq in arquivos:
                if arq.exists():
                    zf.write(arq, f"{pasta_zip}/{arq.name}")
                else:
                    log.warn(f"Arquivo não encontrado, ignorado: {arq.name}")

        # Remover ZIP antigo se diferente do novo
        if ZIP_FILE.exists() and ZIP_FILE != nome_zip:
            ZIP_FILE.unlink()

        # Atualizar referência do ZIP padrão
        if nome_zip != ZIP_FILE:
            shutil.copy2(nome_zip, ZIP_FILE)

        tamanho = nome_zip.stat().st_size / 1024 / 1024
        log.ok(f"ZIP recriado: {nome_zip.name} ({tamanho:.1f} MB)")
        return True

    except Exception as e:
        log.erro(f"Falha ao recriar ZIP: {e}")
        return False


# ─── Etapa 5: Commit e Push ───────────────────────────────────────────────────

def git_commit_push(versao: str, total: int) -> bool:
    """Faz commit e push das alterações para o GitHub."""
    mensagem = (
        f"chore: Atualiza dados TUSS para versao {versao}\n\n"
        f"- Total de registros: {total}\n"
        f"- Data de atualizacao: {datetime.now().strftime('%d/%m/%Y')}\n"
        f"- Arquivos atualizados: JSON, HTML, ZIP"
    )

    etapas = [
        (["git", "add", "."],                     "Staging dos arquivos"),
        (["git", "commit", "-m", mensagem],        "Commit"),
        (["git", "push", "origin", "HEAD"],        "Push para GitHub"),
    ]

    for cmd, desc in etapas:
        log.info(f"{desc}...")
        if not executar(cmd, desc):
            return False
        log.ok(desc)

    return True


# ─── Verificação de integridade ───────────────────────────────────────────────

def verificar_repositorio():
    """Verifica o estado atual do repositório e dos dados."""
    print("\n" + "=" * 70)
    print("  VERIFICAÇÃO DO REPOSITÓRIO")
    print("=" * 70 + "\n")

    arquivos = {
        "HTML interativo":  HTML_FILE,
        "Dados JSON":       JSON_FILE,
        "Pacote ZIP":       ZIP_FILE,
        "Instalador PY":    REPO_DIR / "instalador_tuss.py",
        "Script Linux/Mac": REPO_DIR / "instalar_tuss.sh",
        "Script BAT":       REPO_DIR / "compilar_exe.bat",
        "README":           REPO_DIR / "README.md",
        "Guia Instalação":  REPO_DIR / "GUIA_INSTALACAO.md",
    }

    todos_ok = True
    for nome, caminho in arquivos.items():
        if caminho.exists():
            tam = caminho.stat().st_size / 1024
            print(f"  ✓ {nome:<25} {caminho.name:<45} {tam:>8.1f} KB")
        else:
            print(f"  ✗ {nome:<25} AUSENTE")
            todos_ok = False

    # Verificar JSON
    if JSON_FILE.exists():
        try:
            with open(JSON_FILE, encoding="utf-8") as f:
                dados = json.load(f)
            meta = dados.get("metadata", {})
            print(f"\n  📊 Dados JSON:")
            print(f"     Versão:          {meta.get('versao', 'N/A')}")
            print(f"     Última atualização: {meta.get('data_atualizacao', 'N/A')}")
            print(f"     Total de registros: {meta.get('total_registros', 'N/A')}")
            print(f"     Com correlação:  {meta.get('com_correlacao', 'N/A')}")
            print(f"     Sem correlação:  {meta.get('sem_correlacao', 'N/A')}")
        except Exception as e:
            print(f"\n  ⚠ Erro ao ler JSON: {e}")

    # Verificar Git
    resultado = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        capture_output=True, text=True, cwd=REPO_DIR
    )
    if resultado.returncode == 0:
        print(f"\n  📝 Últimos commits:")
        for linha in resultado.stdout.strip().split("\n"):
            print(f"     {linha}")

    print()
    if todos_ok:
        print("  ✅ Repositório íntegro e pronto para uso.\n")
    else:
        print("  ⚠  Alguns arquivos estão ausentes. Execute a atualização.\n")


# ─── Fluxo principal ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Atualiza os dados TUSS no repositório GitHub.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--arquivo", "-a",
        type=Path,
        help="Caminho para o novo arquivo Excel (.xlsx) da ANS",
    )
    parser.add_argument(
        "--versao", "-v",
        default=datetime.now().strftime("%Y.%m"),
        help="Versão dos dados (padrão: AAAA.MM)",
    )
    parser.add_argument(
        "--sem-push",
        action="store_true",
        help="Executa todas as etapas sem fazer push para o GitHub",
    )
    parser.add_argument(
        "--verificar",
        action="store_true",
        help="Apenas verifica o estado atual do repositório",
    )

    args = parser.parse_args()

    print("\n" + "=" * 70)
    print("  ATUALIZAÇÃO AUTOMÁTICA - CORRELAÇÃO TUSS")
    print("=" * 70 + "\n")

    if args.verificar:
        verificar_repositorio()
        return

    if not args.arquivo:
        parser.print_help()
        print("\n❌ Informe o arquivo Excel com --arquivo caminho/para/arquivo.xlsx\n")
        sys.exit(1)

    if not args.arquivo.exists():
        log.erro(f"Arquivo não encontrado: {args.arquivo}")
        sys.exit(1)

    total_etapas = 4 if args.sem_push else 5
    versao = args.versao

    log.info(f"Versão alvo: {versao}")
    log.info(f"Push ao GitHub: {'NÃO' if args.sem_push else 'SIM'}")
    print()

    # ── Etapa 1: Converter Excel → JSON
    log.step(1, total_etapas, "Convertendo Excel para JSON...")
    dados = converter_excel_para_json(args.arquivo, versao)
    if not dados:
        sys.exit(1)

    # ── Etapa 2: Salvar JSON
    log.step(2, total_etapas, "Salvando JSON...")
    if not salvar_json(dados):
        sys.exit(1)

    # ── Etapa 3: Regenerar HTML
    log.step(3, total_etapas, "Regenerando tabela HTML...")
    if not regenerar_html(dados):
        sys.exit(1)

    # ── Etapa 4: Recriar ZIP
    log.step(4, total_etapas, "Recriando pacote ZIP...")
    if not recriar_zip(versao):
        sys.exit(1)

    # ── Etapa 5: Commit e Push
    if not args.sem_push:
        log.step(5, total_etapas, "Enviando para o GitHub...")
        if not git_commit_push(versao, dados["metadata"]["total_registros"]):
            log.warn("Push falhou. Verifique as credenciais do Git e tente manualmente.")
        else:
            log.ok("Push realizado com sucesso!")

    print()
    print("=" * 70)
    print("  ✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    print(f"\n  Versão:    {versao}")
    print(f"  Registros: {dados['metadata']['total_registros']}")
    print(f"  JSON:      {JSON_FILE.name}")
    print(f"  HTML:      {HTML_FILE.name}")
    print(f"  ZIP:       Correlacao_TUSS_{versao}.zip")
    if not args.sem_push:
        print(f"  GitHub:    https://github.com/lzacher/correlacao-tuss")
    print()


if __name__ == "__main__":
    main()
