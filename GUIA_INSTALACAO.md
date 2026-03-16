# Guia de Instalação - Correlação TUSS v1.0

## 📋 Visão Geral

Este guia fornece instruções para instalar a **Tabela de Correlação TUSS** em diferentes sistemas operacionais. A tabela é uma aplicação web interativa que funciona em qualquer navegador moderno.

---

## 🖥️ Requisitos do Sistema

### Mínimos
- **Navegador web**: Chrome, Firefox, Safari, Edge (versão recente)
- **Espaço em disco**: ~5 MB
- **Memória RAM**: 512 MB (recomendado 1 GB ou mais)
- **Conexão de internet**: Não é necessária

### Sistemas Operacionais Suportados
- ✅ Windows 7, 8, 10, 11
- ✅ macOS 10.12 ou superior
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

---

## 🚀 Instalação no Windows

### Opção 1: Usando o Instalador Python (Recomendado)

#### Pré-requisitos
- Python 3.6 ou superior instalado
- Pacote `pywin32` (para criar atalhos)

#### Passos

1. **Baixe os arquivos**
   - `instalador_tuss.py`
   - `CorrelacaoTUSS_Interativa.html`
   - `CorrelacaoTUSS_2025.json`

2. **Coloque os arquivos na mesma pasta**

3. **Abra o Prompt de Comando (CMD)**
   - Pressione `Win + R`
   - Digite `cmd` e pressione Enter

4. **Navegue até a pasta dos arquivos**
   ```bash
   cd C:\Caminho\Para\Pasta
   ```

5. **Execute o instalador**
   ```bash
   python instalador_tuss.py
   ```

6. **Siga as instruções na tela**
   - Escolha o local de instalação
   - Aguarde a conclusão
   - Opcionalmente, abra a tabela automaticamente

#### Resultado
- ✓ Arquivos instalados no diretório escolhido
- ✓ Atalho criado na Área de Trabalho (opcional)
- ✓ Arquivo README com instruções

### Opção 2: Instalação Manual

1. **Crie uma pasta** para a aplicação
   - Exemplo: `C:\Users\SeuUsuário\Desktop\Correlação TUSS`

2. **Copie os arquivos** para a pasta
   - `CorrelacaoTUSS_Interativa.html`
   - `CorrelacaoTUSS_2025.json`

3. **Crie um atalho**
   - Clique com botão direito no arquivo HTML
   - Selecione "Enviar para" → "Área de Trabalho (criar atalho)"

4. **Abra a tabela**
   - Clique duas vezes no arquivo HTML ou no atalho
   - Ele abrirá no seu navegador padrão

---

## 🍎 Instalação no macOS

### Opção 1: Usando o Script de Instalação

#### Pré-requisitos
- Terminal (já incluído no macOS)
- Permissão para executar scripts

#### Passos

1. **Baixe os arquivos**
   - `instalar_tuss.sh`
   - `CorrelacaoTUSS_Interativa.html`
   - `CorrelacaoTUSS_2025.json`

2. **Abra o Terminal**
   - Pressione `Cmd + Espaço`
   - Digite `Terminal` e pressione Enter

3. **Navegue até a pasta dos arquivos**
   ```bash
   cd /Caminho/Para/Pasta
   ```

4. **Dê permissão de execução ao script**
   ```bash
   chmod +x instalar_tuss.sh
   ```

5. **Execute o instalador**
   ```bash
   ./instalar_tuss.sh
   ```

6. **Siga as instruções na tela**

#### Resultado
- ✓ Arquivos instalados em `~/Documents/Correlação TUSS`
- ✓ Arquivos de informação criados
- ✓ Tabela pronta para uso

### Opção 2: Instalação Manual

1. **Crie uma pasta** em Documentos
   - `Correlação TUSS`

2. **Copie os arquivos** para a pasta
   - `CorrelacaoTUSS_Interativa.html`
   - `CorrelacaoTUSS_2025.json`

3. **Abra a tabela**
   - Clique duas vezes no arquivo HTML
   - Ele abrirá no seu navegador padrão

---

## 🐧 Instalação no Linux

### Opção 1: Usando o Script de Instalação (Recomendado)

#### Pré-requisitos
- Terminal (já incluído em todas as distribuições)
- Bash shell

#### Passos

1. **Baixe os arquivos**
   - `instalar_tuss.sh`
   - `CorrelacaoTUSS_Interativa.html`
   - `CorrelacaoTUSS_2025.json`

2. **Abra o Terminal**
   - Pressione `Ctrl + Alt + T` (na maioria das distribuições)

3. **Navegue até a pasta dos arquivos**
   ```bash
   cd ~/Downloads  # ou o caminho onde você baixou
   ```

4. **Dê permissão de execução ao script**
   ```bash
   chmod +x instalar_tuss.sh
   ```

5. **Execute o instalador**
   ```bash
   ./instalar_tuss.sh
   ```

6. **Siga as instruções na tela**

#### Resultado
- ✓ Arquivos instalados em `~/Documentos/Correlação TUSS`
- ✓ Atalho criado no menu de aplicativos
- ✓ Arquivos de informação criados

### Opção 2: Instalação Manual

1. **Crie uma pasta** em Documentos
   ```bash
   mkdir -p ~/Documentos/Correlação\ TUSS
   ```

2. **Copie os arquivos** para a pasta
   ```bash
   cp CorrelacaoTUSS_Interativa.html ~/Documentos/Correlação\ TUSS/
   cp CorrelacaoTUSS_2025.json ~/Documentos/Correlação\ TUSS/
   ```

3. **Abra a tabela**
   ```bash
   xdg-open ~/Documentos/Correlação\ TUSS/CorrelacaoTUSS_Interativa.html
   ```

---

## 📖 Como Usar a Tabela

### Abrindo a Tabela
1. Localize o arquivo `CorrelacaoTUSS_Interativa.html`
2. Clique duas vezes para abrir no navegador
3. A tabela carregará com todos os 6.735 registros

### Funcionalidades Principais

#### 🔍 Busca
- Digite na barra de pesquisa para buscar por:
  - Código TUSS
  - Terminologia do procedimento
  - Descrição do procedimento
  - Subgrupo, grupo ou capítulo

#### 🏷️ Filtros
- **Todos**: Exibe todos os registros
- **Com Correlação**: Mostra apenas procedimentos com correlação (SIM)
- **Sem Correlação**: Mostra apenas procedimentos sem correlação (NÃO)

#### 📊 Ordenação
- Clique em qualquer cabeçalho de coluna para ordenar
- Clique novamente para inverter a ordem

#### ✕ Limpar Pesquisa
- Clique no botão "✕ Limpar" para remover a busca

#### 📈 Estatísticas
- O painel superior mostra:
  - Total de registros
  - Quantidade com correlação
  - Quantidade sem correlação
  - Registros atualmente exibidos

---

## 🔧 Solução de Problemas

### Problema: "Arquivo não encontrado"
**Solução**: Certifique-se de que todos os arquivos estão na mesma pasta

### Problema: "Permissão negada" (Linux/Mac)
**Solução**: Execute `chmod +x instalar_tuss.sh` antes de executar

### Problema: A tabela não abre no navegador
**Solução**: 
1. Abra o navegador manualmente
2. Pressione `Ctrl + O` (ou `Cmd + O` no Mac)
3. Selecione o arquivo `CorrelacaoTUSS_Interativa.html`

### Problema: Dados não aparecem
**Solução**: Certifique-se de que o arquivo `CorrelacaoTUSS_2025.json` está na mesma pasta que o HTML

### Problema: Navegador antigo não funciona
**Solução**: Atualize seu navegador para a versão mais recente

---

## 📦 Arquivos Inclusos

| Arquivo | Descrição |
|---------|-----------|
| `CorrelacaoTUSS_Interativa.html` | Tabela interativa (arquivo principal) |
| `CorrelacaoTUSS_2025.json` | Dados em formato JSON |
| `instalador_tuss.py` | Instalador para Windows |
| `instalar_tuss.sh` | Instalador para Linux/Mac |
| `INFO.json` | Informações sobre a instalação |
| `LEIAME.txt` | Instruções de uso |
| `GUIA_INSTALACAO.md` | Este arquivo |

---

## 🌐 Requisitos de Navegador

| Navegador | Versão Mínima | Status |
|-----------|---------------|--------|
| Chrome | 60+ | ✅ Totalmente suportado |
| Firefox | 55+ | ✅ Totalmente suportado |
| Safari | 11+ | ✅ Totalmente suportado |
| Edge | 79+ | ✅ Totalmente suportado |
| Internet Explorer | - | ❌ Não suportado |

---

## 📞 Suporte

### Para dúvidas sobre a instalação
- Consulte este guia
- Verifique se todos os arquivos estão presentes
- Certifique-se de que seu navegador é moderno

### Para dúvidas sobre os dados
- Consulte: https://www.gov.br/ans/pt-br
- Fonte: ANS - Agência Nacional de Saúde Suplementar
- Data de publicação: 17/02/2025

---

## 📋 Informações da Aplicação

| Campo | Valor |
|-------|-------|
| **Nome** | Correlação TUSS |
| **Versão** | 1.0 |
| **Total de Registros** | 6.735 |
| **Fonte** | ANS - Agência Nacional de Saúde Suplementar |
| **Data de Publicação** | 17/02/2025 |
| **Descrição** | Tabela de Correlação entre Terminologia de Procedimentos e Eventos em Saúde e o Rol RN 465/2021 |

---

## ✅ Checklist de Instalação

- [ ] Todos os arquivos foram baixados
- [ ] Os arquivos estão na mesma pasta
- [ ] O navegador está atualizado
- [ ] A instalação foi concluída com sucesso
- [ ] A tabela abre no navegador
- [ ] Os dados aparecem corretamente
- [ ] A busca funciona
- [ ] Os filtros funcionam
- [ ] A ordenação funciona

---

## 📝 Notas Importantes

1. **Sem conexão de internet necessária**: A tabela funciona completamente offline
2. **Dados locais**: Todos os dados são armazenados localmente no seu computador
3. **Segurança**: Nenhum dado é enviado para servidores externos
4. **Compatibilidade**: Funciona em qualquer navegador moderno
5. **Portabilidade**: Você pode copiar a pasta de instalação para outro computador

---

**Versão do Guia**: 1.0  
**Última atualização**: 15/03/2026  
**Desenvolvido por**: Manus
