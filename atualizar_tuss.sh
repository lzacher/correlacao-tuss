#!/bin/bash
# =============================================================================
# Wrapper de Atualização TUSS para Linux/Mac
# Verifica dependências e executa o script Python principal
# =============================================================================

set -e

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $1"; }
erro() { echo -e "${RED}✗${NC} $1"; exit 1; }
info() { echo -e "${BLUE}ℹ${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "============================================================================"
echo -e "  ${BLUE}Atualização Automática - Correlação TUSS${NC}"
echo "============================================================================"
echo ""

# Verificar Python
if ! command -v python3 &>/dev/null; then
    erro "Python 3 não encontrado. Instale com: sudo apt install python3"
fi
ok "Python encontrado: $(python3 --version)"

# Verificar dependências Python
info "Verificando dependências Python..."
python3 -c "import pandas, openpyxl" 2>/dev/null || {
    warn "Instalando dependências necessárias..."
    pip3 install pandas openpyxl --quiet
    ok "Dependências instaladas"
}
ok "Dependências OK"

# Verificar Git
if ! command -v git &>/dev/null; then
    erro "Git não encontrado. Instale com: sudo apt install git"
fi
ok "Git encontrado: $(git --version)"

echo ""

# Repassar todos os argumentos para o script Python
python3 "$SCRIPT_DIR/atualizar_tuss.py" "$@"
