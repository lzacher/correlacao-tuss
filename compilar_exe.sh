#!/bin/bash

# ============================================================================
# Script para compilar o instalador TUSS para EXE no Linux/Mac
# ============================================================================

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Funções
print_header() {
    echo ""
    echo "============================================================================"
    echo -e "  ${BLUE}Compilador de EXE - Correlação TUSS${NC}"
    echo "============================================================================"
    echo ""
}

print_step() {
    echo -e "${BLUE}[$1]${NC} $2"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Verificar se Python está instalado
check_python() {
    print_step "1/5" "Verificando Python..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 não encontrado!"
        echo ""
        echo "Por favor, instale Python 3.6 ou superior:"
        echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
        echo "  macOS: brew install python3"
        exit 1
    fi
    
    python3 --version
    print_success "Python encontrado"
}

# Instalar PyInstaller
install_pyinstaller() {
    print_step "2/5" "Instalando PyInstaller..."
    
    if ! pip3 install pyinstaller --quiet; then
        print_error "Falha ao instalar PyInstaller"
        exit 1
    fi
    
    print_success "PyInstaller instalado"
}

# Instalar dependências do sistema
install_system_deps() {
    print_step "3/5" "Verificando dependências do sistema..."
    
    local sistema=$(uname)
    
    if [ "$sistema" = "Linux" ]; then
        if ! command -v objdump &> /dev/null; then
            print_warning "binutils não encontrado, instalando..."
            sudo apt-get update -qq
            sudo apt-get install -y binutils libpython3.11 &> /dev/null
            print_success "Dependências instaladas"
        else
            print_success "Dependências encontradas"
        fi
    elif [ "$sistema" = "Darwin" ]; then
        print_success "macOS detectado"
    fi
}

# Compilar EXE
compile_exe() {
    print_step "4/5" "Compilando instalador para EXE..."
    echo "Isso pode levar alguns minutos..."
    echo ""
    
    pyinstaller --onefile \
        --windowed \
        --name "Instalador Correlação TUSS" \
        --add-data "CorrelacaoTUSS_Interativa.html:." \
        --add-data "CorrelacaoTUSS_2025.json:." \
        --distpath ./dist \
        --workpath ./build \
        --specpath ./spec \
        instalador_tuss.py 2>&1 | grep -E "(INFO|ERROR)" | tail -10
    
    print_success "Compilação concluída"
}

# Verificar resultado
check_result() {
    print_step "5/5" "Finalizando..."
    echo ""
    
    if [ -f "dist/Instalador Correlação TUSS" ]; then
        local tamanho=$(ls -lh "dist/Instalador Correlação TUSS" | awk '{print $5}')
        
        echo "============================================================================"
        echo -e "${GREEN}✓ SUCESSO! EXE criado com sucesso!${NC}"
        echo "============================================================================"
        echo ""
        echo "Arquivo gerado: dist/Instalador Correlação TUSS"
        echo "Tamanho: $tamanho"
        echo ""
        echo "Você pode agora distribuir este arquivo junto com:"
        echo "  - CorrelacaoTUSS_Interativa.html"
        echo "  - CorrelacaoTUSS_2025.json"
        echo ""
        echo "Ou copiar apenas o EXE para a pasta 'dist' e distribuir tudo junto."
        echo ""
    else
        print_error "EXE não foi criado"
        exit 1
    fi
}

# Executar
main() {
    print_header
    
    check_python
    echo ""
    
    install_pyinstaller
    echo ""
    
    install_system_deps
    echo ""
    
    compile_exe
    echo ""
    
    check_result
}

main
