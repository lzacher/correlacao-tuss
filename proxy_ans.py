#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
proxy_ans.py
============
Servidor proxy local que permite ao HTML consultar o site da ANS sem
bloqueio de CORS (Cross-Origin Resource Sharing).

O navegador não consegue fazer requisições diretamente ao gov.br por
restrições de segurança. Este proxy recebe a requisição do HTML,
consulta a ANS e devolve o resultado.

Uso:
  python proxy_ans.py          # Inicia na porta 5000
  python proxy_ans.py --porta 8081

Endpoints:
  GET /verificar   → retorna JSON com nome e URL do arquivo mais recente na ANS
  GET /baixar      → baixa e retorna o XLSX mais recente da ANS
  GET /status      → verifica se o proxy está rodando

Requisitos:
  pip install flask requests beautifulsoup4
"""

import os
import sys
import argparse
import tempfile
from pathlib import Path

try:
    from flask import Flask, jsonify, send_file, request
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERRO] Instale: pip install flask requests beautifulsoup4")
    sys.exit(1)

# ─── Configurações ─────────────────────────────────────────────────────────────

ANS_PAGINA  = (
    "https://www.gov.br/ans/pt-br/acesso-a-informacao/"
    "participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
)
ANS_BASE_URL = "https://www.gov.br"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Referer": ANS_PAGINA,
}

app = Flask(__name__)


def cors(resp):
    """Adiciona cabeçalhos CORS para permitir acesso do HTML local."""
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


def detectar_arquivo_ans():
    """Detecta o arquivo XLSX mais recente na página da ANS."""
    r = requests.get(ANS_PAGINA, headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    candidatos = []
    for a in soup.find_all("a", href=True):
        href  = a["href"]
        nome  = os.path.basename(href.split("?")[0]).rstrip("/")
        lower = nome.lower()
        if (("correlac" in lower or "correla" in lower)
                and "tuss" in lower
                and (lower.endswith(".xlsx") or lower.endswith(".xls"))):
            base   = href.rstrip("/").replace("/view", "").replace("/@@download/file", "")
            url_dl = (base if base.startswith("http") else ANS_BASE_URL + base) + "/@@download/file"
            candidatos.append({"nome": nome, "url": url_dl})

    if not candidatos:
        return None

    # Remover duplicatas e retornar o mais recente (maior nome = mais recente)
    vistos, unicos = set(), []
    for c in candidatos:
        if c["nome"] not in vistos:
            vistos.add(c["nome"])
            unicos.append(c)
    unicos.sort(key=lambda x: x["nome"], reverse=True)
    return unicos


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.route("/status")
def status():
    return cors(jsonify({"ok": True, "proxy": "proxy_ans.py", "versao": "1.0"}))


@app.route("/verificar")
def verificar():
    """Retorna lista de arquivos disponíveis na ANS."""
    try:
        arquivos = detectar_arquivo_ans()
        if not arquivos:
            return cors(jsonify({"erro": "Nenhum arquivo encontrado na página da ANS."})), 404
        return cors(jsonify({
            "ok":        True,
            "mais_recente": arquivos[0],
            "todos":     arquivos[:5],
            "pagina_ans": ANS_PAGINA,
        }))
    except Exception as e:
        return cors(jsonify({"erro": str(e)})), 500


@app.route("/baixar")
def baixar():
    """Baixa e retorna o XLSX mais recente da ANS."""
    try:
        arquivos = detectar_arquivo_ans()
        if not arquivos:
            return cors(jsonify({"erro": "Nenhum arquivo encontrado."})), 404

        url  = arquivos[0]["url"]
        nome = arquivos[0]["nome"]

        r = requests.get(url, headers=HEADERS, stream=True, timeout=60)
        r.raise_for_status()

        # Salvar em arquivo temporário e enviar ao navegador
        sufixo = ".xlsx" if nome.lower().endswith(".xlsx") else ".xls"
        tmp = tempfile.NamedTemporaryFile(suffix=sufixo, delete=False)
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                tmp.write(chunk)
        tmp.close()

        return cors(send_file(
            tmp.name,
            as_attachment=True,
            download_name=nome,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ))
    except Exception as e:
        return cors(jsonify({"erro": str(e)})), 500


@app.route("/options", methods=["OPTIONS"])
@app.route("/verificar", methods=["OPTIONS"])
@app.route("/baixar", methods=["OPTIONS"])
def options():
    return cors(app.make_response(("", 204)))


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy local para consulta à ANS.")
    parser.add_argument("--porta", "-p", type=int, default=5000,
                        help="Porta do servidor (padrão: 5000)")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Host do servidor (padrão: 127.0.0.1)")
    args = parser.parse_args()

    print(f"\n{'='*55}")
    print(f"  PROXY ANS — Correlação TUSS")
    print(f"{'='*55}")
    print(f"  Rodando em: http://{args.host}:{args.porta}")
    print(f"  Endpoints:")
    print(f"    GET /status    → verifica se o proxy está ativo")
    print(f"    GET /verificar → detecta versão mais recente na ANS")
    print(f"    GET /baixar    → baixa o XLSX mais recente da ANS")
    print(f"\n  Mantenha esta janela aberta enquanto usa o HTML.")
    print(f"  Pressione Ctrl+C para encerrar.")
    print(f"{'='*55}\n")

    app.run(host=args.host, port=args.porta, debug=False)
