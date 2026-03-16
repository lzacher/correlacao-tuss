#!/bin/bash

# Instalador da Tabela de Correlação TUSS para Linux/Mac
# Versão 1.0
# Descrição: Instala a tabela HTML interativa de correlação TUSS

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variáveis
APP_NAME="Correlação TUSS"
APP_VERSION="1.0"
HTML_FILE="CorrelacaoTUSS_Interativa.html"
JSON_FILE="CorrelacaoTUSS_2025.json"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Função para exibir cabeçalho
exibir_cabecalho() {
    clear
    echo "================================================================================"
    echo "  ${BLUE}${APP_NAME} - Instalador v${APP_VERSION}${NC}"
    echo "================================================================================"
    echo ""
    echo "  Tabela de Correlação entre Terminologia de Procedimentos"
    echo "  e Eventos em Saúde - Rol RN 465/2021"
    echo ""
    echo "  Publicado em 17/02/2025"
    echo "  ANS - Agência Nacional de Saúde Suplementar"
    echo ""
    echo "================================================================================"
    echo ""
}

# Função para exibir mensagem de sucesso
sucesso() {
    echo -e "${GREEN}✓${NC} $1"
}

# Função para exibir mensagem de erro
erro() {
    echo -e "${RED}❌${NC} $1"
}

# Função para exibir aviso
aviso() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Função para exibir informação
info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Verificar se os arquivos existem
verificar_arquivos() {
    if [ ! -f "$SCRIPT_DIR/$HTML_FILE" ]; then
        erro "Arquivo '$HTML_FILE' não encontrado!"
        erro "Procurado em: $SCRIPT_DIR/$HTML_FILE"
        exit 1
    fi
    
    if [ ! -f "$SCRIPT_DIR/$JSON_FILE" ]; then
        aviso "Arquivo '$JSON_FILE' não encontrado!"
        aviso "A tabela funcionará, mas sem os dados atualizados"
    fi
}

# Obter caminho de instalação
obter_caminho_instalacao() {
    local sistema=$(uname)
    
    if [ "$sistema" = "Darwin" ]; then
        # macOS
        local caminho_padrao="$HOME/Documents/Correlação TUSS"
    else
        # Linux
        local caminho_padrao="$HOME/Documentos/Correlação TUSS"
    fi
    
    echo ""
    echo "📁 SELEÇÃO DO DIRETÓRIO DE INSTALAÇÃO"
    echo "------------------------------------------------------------------------"
    echo ""
    echo "Caminho padrão sugerido:"
    echo "  $caminho_padrao"
    echo ""
    
    read -p "Deseja instalar neste local? (S/n): " resposta
    resposta=${resposta:-s}
    
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        echo "$caminho_padrao"
    else
        read -p "Digite o caminho completo desejado: " caminho_personalizado
        echo "$caminho_personalizado"
    fi
}

# Criar diretório
criar_diretorio() {
    local caminho="$1"
    
    if mkdir -p "$caminho"; then
        sucesso "Diretório criado: $caminho"
        return 0
    else
        erro "Erro ao criar diretório: $caminho"
        return 1
    fi
}

# Copiar arquivo HTML
copiar_arquivo_html() {
    local origem="$1"
    local destino="$2"
    
    if cp "$origem" "$destino/$HTML_FILE"; then
        sucesso "Arquivo HTML instalado: $destino/$HTML_FILE"
        return 0
    else
        erro "Erro ao copiar arquivo HTML"
        return 1
    fi
}

# Copiar arquivo JSON
copiar_arquivo_json() {
    local origem="$1"
    local destino="$2"
    
    if [ -f "$origem" ]; then
        if cp "$origem" "$destino/$JSON_FILE"; then
            sucesso "Arquivo JSON instalado: $destino/$JSON_FILE"
            return 0
        else
            aviso "Erro ao copiar arquivo JSON"
            return 0  # Não é crítico
        fi
    fi
    return 0
}

# Criar arquivo de informações
criar_arquivo_info() {
    local destino="$1"
    local data_instalacao=$(date '+%Y-%m-%d %H:%M:%S')
    
    cat > "$destino/INFO.txt" << EOF
================================================================================
${APP_NAME} v${APP_VERSION}
================================================================================

DESCRIÇÃO:
Tabela de Correlação entre Terminologia de Procedimentos e Eventos em Saúde
e o Rol de Procedimentos e Eventos em Saúde RN nº 465/2021 e suas alterações.

ARQUIVOS INCLUSOS:
- ${HTML_FILE}: Tabela interativa (abrir no navegador)
- ${JSON_FILE}: Dados em formato JSON
- INFO.txt: Este arquivo
- LEIAME.txt: Instruções de uso

COMO USAR:
1. Abra o arquivo "${HTML_FILE}" em qualquer navegador web
2. Use a barra de pesquisa para buscar procedimentos
3. Clique nos cabeçalhos para ordenar os dados
4. Use os filtros para refinar os resultados

FUNCIONALIDADES:
✓ Busca em tempo real
✓ Filtros por correlação (SIM/NÃO)
✓ Ordenação por coluna
✓ Indicadores de cobertura (OD, AMB, HCO, HSO, PAC, DUT)
✓ Painel de estatísticas
✓ Design responsivo (funciona em celulares e tablets)

REQUISITOS:
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Sem necessidade de conexão com a internet

FONTE:
ANS - Agência Nacional de Saúde Suplementar
Publicado em: 17/02/2025

SUPORTE:
Para dúvidas sobre os dados, consulte:
https://www.gov.br/ans/pt-br

================================================================================
Instalado em: ${data_instalacao}
================================================================================
EOF
    
    sucesso "Arquivo de informações criado"
}

# Criar arquivo LEIAME
criar_arquivo_leiame() {
    local destino="$1"
    
    cat > "$destino/LEIAME.txt" << 'EOF'
# Correlação TUSS v1.0

## Descrição
Tabela de Correlação entre Terminologia de Procedimentos e Eventos em Saúde
e o Rol de Procedimentos e Eventos em Saúde RN nº 465/2021 e suas alterações.

## Como Usar

### Abrir a Tabela
1. Abra o arquivo "CorrelacaoTUSS_Interativa.html" em seu navegador web favorito
2. A tabela carregará com todos os 6.735 registros

### Buscar Procedimentos
- Digite na barra de pesquisa para buscar por:
  * Código TUSS
  * Terminologia do procedimento
  * Descrição do procedimento
  * Subgrupo, grupo ou capítulo

### Filtrar Resultados
- Clique em "Todos" para ver todos os registros
- Clique em "Com Correlação" para ver apenas procedimentos com correlação (SIM)
- Clique em "Sem Correlação" para ver apenas procedimentos sem correlação (NÃO)

### Ordenar Dados
- Clique em qualquer cabeçalho de coluna para ordenar
- Clique novamente para inverter a ordem (ascendente/descendente)

### Limpar Pesquisa
- Clique no botão "✕ Limpar" para remover a busca e voltar à exibição completa

## Indicadores de Cobertura
- OD: Odontologia
- AMB: Ambulatorial
- HCO: Hospital com Cirurgia
- HSO: Hospital sem Cirurgia
- PAC: Pronto Atendimento/Clínica
- DUT: Diária UTI

## Painel de Estatísticas
O painel superior exibe em tempo real:
- Total de registros na base
- Quantidade com correlação
- Quantidade sem correlação
- Registros atualmente exibidos

## Requisitos
- Navegador web moderno (Chrome, Firefox, Safari, Edge)
- Sem necessidade de conexão com a internet

## Fonte
ANS - Agência Nacional de Saúde Suplementar
Publicado em: 17/02/2025

## Suporte
Para dúvidas sobre os dados, consulte:
https://www.gov.br/ans/pt-br
EOF
    
    sucesso "Arquivo LEIAME.txt criado"
}

# Criar atalho no menu de aplicativos (Linux)
criar_atalho_linux() {
    local destino="$1"
    local arquivo_html="$destino/$HTML_FILE"
    local desktop_dir="$HOME/.local/share/applications"
    
    if [ -d "$desktop_dir" ]; then
        cat > "$desktop_dir/correlacao-tuss.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Correlação TUSS
Comment=Tabela de Correlação TUSS - Rol RN 465/2021
Exec=xdg-open "$arquivo_html"
Icon=text-html
Categories=Office;Spreadsheet;
Terminal=false
EOF
        sucesso "Atalho criado no menu de aplicativos"
    fi
}

# Função principal
main() {
    exibir_cabecalho
    
    # Verificar arquivos
    verificar_arquivos
    
    # Obter caminho de instalação
    CAMINHO_INSTALACAO=$(obter_caminho_instalacao)
    
    echo ""
    echo "📦 INICIANDO INSTALAÇÃO"
    echo "------------------------------------------------------------------------"
    echo ""
    
    # Criar diretório
    if ! criar_diretorio "$CAMINHO_INSTALACAO"; then
        exit 1
    fi
    
    # Copiar arquivos
    if ! copiar_arquivo_html "$SCRIPT_DIR/$HTML_FILE" "$CAMINHO_INSTALACAO"; then
        exit 1
    fi
    
    copiar_arquivo_json "$SCRIPT_DIR/$JSON_FILE" "$CAMINHO_INSTALACAO"
    
    # Criar arquivos adicionais
    criar_arquivo_info "$CAMINHO_INSTALACAO"
    criar_arquivo_leiame "$CAMINHO_INSTALACAO"
    
    # Criar atalho (Linux)
    if [ "$(uname)" != "Darwin" ]; then
        criar_atalho_linux "$CAMINHO_INSTALACAO"
    fi
    
    # Sucesso
    echo ""
    echo "================================================================================"
    echo -e "${GREEN}✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!${NC}"
    echo "================================================================================"
    echo ""
    echo "Local de instalação: $CAMINHO_INSTALACAO"
    echo ""
    
    # Perguntar se deseja abrir
    read -p "Deseja abrir a tabela agora? (S/n): " abrir_agora
    abrir_agora=${abrir_agora:-s}
    
    if [ "$abrir_agora" = "s" ] || [ "$abrir_agora" = "S" ]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open "$CAMINHO_INSTALACAO/$HTML_FILE" &
            sucesso "Abrindo no navegador..."
        elif command -v open &> /dev/null; then
            open "$CAMINHO_INSTALACAO/$HTML_FILE"
            sucesso "Abrindo no navegador..."
        else
            aviso "Não foi possível abrir automaticamente"
            info "Abra manualmente: $CAMINHO_INSTALACAO/$HTML_FILE"
        fi
    fi
    
    echo ""
}

# Executar
main
