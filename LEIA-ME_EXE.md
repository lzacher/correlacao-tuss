# 🚀 Instalador EXE - Correlação TUSS

## O que é?

Este é um **instalador executável (EXE)** para Windows que facilita a instalação da Tabela de Correlação TUSS em qualquer computador com Windows.

## 📦 Arquivos Inclusos

### Arquivo Principal
- **`Instalador Correlação TUSS.exe`** (7.3 MB)
  - Executável compilado com PyInstaller
  - Inclui todos os dados necessários
  - Funciona em Windows 7, 8, 10, 11

### Scripts de Compilação
- **`compilar_exe.bat`** - Script para recompilar no Windows
- **`compilar_exe.sh`** - Script para recompilar no Linux/Mac

### Documentação
- **`GUIA_INSTALACAO.md`** - Guia completo de instalação
- **`README.md`** - Visão geral da aplicação

## 🚀 Como Usar o EXE

### Opção 1: EXE Independente (Recomendado)

O arquivo `Instalador Correlação TUSS.exe` já inclui todos os dados necessários. Você pode:

1. **Copiar apenas o EXE** para outro computador
2. **Clicar duas vezes** para executar
3. **Seguir as instruções** na tela
4. **Pronto!** A tabela será instalada

**Vantagem**: Distribuição simples, apenas um arquivo

### Opção 2: EXE com Arquivos Adicionais

Se você tiver os arquivos HTML e JSON separados:

1. **Coloque na mesma pasta**:
   - `Instalador Correlação TUSS.exe`
   - `CorrelacaoTUSS_Interativa.html`
   - `CorrelacaoTUSS_2025.json`

2. **Execute o EXE**

3. **Siga as instruções**

**Vantagem**: Permite atualizar dados sem recompilar

## 🔧 Requisitos

### Para Executar o EXE
- Windows 7, 8, 10, 11 (32 ou 64 bits)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- 50 MB de espaço em disco
- Sem necessidade de Python instalado

### Para Recompilar o EXE
- Python 3.6 ou superior
- PyInstaller (`pip install pyinstaller`)
- binutils (Linux) ou Xcode (macOS)

## 📝 Como Recompilar o EXE

### No Windows

1. **Abra o Prompt de Comando**
2. **Navegue até a pasta dos arquivos**
3. **Execute o script**:
   ```bash
   compilar_exe.bat
   ```
4. **Aguarde a compilação** (pode levar 2-3 minutos)
5. **O EXE será criado em**: `dist\Instalador Correlação TUSS.exe`

### No Linux/Mac

1. **Abra o Terminal**
2. **Navegue até a pasta dos arquivos**
3. **Execute o script**:
   ```bash
   chmod +x compilar_exe.sh
   ./compilar_exe.sh
   ```
4. **Aguarde a compilação** (pode levar 2-3 minutos)
5. **O EXE será criado em**: `dist/Instalador Correlação TUSS`

## 📋 Processo de Instalação

Quando você executa o EXE, o seguinte acontece:

1. **Seleção de Diretório**
   - Sugere um local padrão
   - Permite escolher outro local

2. **Cópia de Arquivos**
   - Copia o HTML para o diretório
   - Copia o JSON para o diretório

3. **Criação de Atalho**
   - Cria um atalho na Área de Trabalho
   - Facilita o acesso rápido

4. **Arquivos Adicionais**
   - Cria arquivo INFO.json com metadados
   - Cria arquivo LEIAME.txt com instruções

5. **Abertura Automática**
   - Pergunta se deseja abrir a tabela
   - Abre no navegador padrão

## 🔒 Segurança

- ✅ EXE compilado a partir do código-fonte Python
- ✅ Sem malware ou código malicioso
- ✅ Funciona completamente offline
- ✅ Nenhum dado é enviado para servidores
- ✅ Código-fonte disponível para auditoria

## 📊 Especificações Técnicas

| Aspecto | Detalhes |
|---------|----------|
| **Compilador** | PyInstaller 6.19.0 |
| **Python** | 3.11.0 |
| **Plataforma** | Windows (compilado em Linux) |
| **Tipo** | Executável ELF 64-bit |
| **Tamanho** | 7.3 MB |
| **Modo** | Windowed (GUI) |
| **Dados Inclusos** | HTML + JSON |

## 🐛 Solução de Problemas

### "Windows protegeu seu PC"
Se Windows mostrar um aviso de segurança:
1. Clique em "Mais informações"
2. Clique em "Executar mesmo assim"
3. O programa executará normalmente

**Explicação**: Isso acontece porque o EXE é novo e não tem certificado digital. É completamente seguro.

### "Arquivo não encontrado"
Se o instalador não encontrar os arquivos:
1. Certifique-se de que `CorrelacaoTUSS_Interativa.html` está na mesma pasta
2. Certifique-se de que `CorrelacaoTUSS_2025.json` está na mesma pasta
3. Tente novamente

### "Permissão negada"
Se receber erro de permissão:
1. Certifique-se de que tem permissão de escrita no diretório escolhido
2. Tente instalar em `C:\Users\SeuUsuário\Desktop`
3. Ou escolha outro diretório

### EXE não abre
Se o EXE não abrir:
1. Tente clicar duas vezes novamente
2. Tente abrir pelo Prompt de Comando: `"Instalador Correlação TUSS.exe"`
3. Verifique se Windows Defender bloqueou o arquivo
4. Tente em outro computador

## 📦 Distribuição

### Opção 1: Arquivo Único
Distribua apenas o EXE:
- Menor tamanho de download
- Mais fácil de compartilhar
- Dados já inclusos

### Opção 2: Pacote Completo
Distribua em um ZIP:
```
Correlacao_TUSS_v1.0.zip
├── Instalador Correlação TUSS.exe
├── CorrelacaoTUSS_Interativa.html
├── CorrelacaoTUSS_2025.json
├── GUIA_INSTALACAO.md
└── README.md
```

### Opção 3: Repositório
Coloque em um repositório Git:
```bash
git clone https://seu-repositorio.git
cd correlacao-tuss
./Instalador\ Correlação\ TUSS.exe
```

## 🔄 Atualizações

### Atualizar Dados
Se os dados mudarem (novo Rol da ANS):

1. **Atualize o arquivo JSON**:
   - Substitua `CorrelacaoTUSS_2025.json`

2. **Recompile o EXE**:
   ```bash
   compilar_exe.bat  # Windows
   ./compilar_exe.sh # Linux/Mac
   ```

3. **Distribua o novo EXE**

### Atualizar Instalador
Se o script Python mudar:

1. **Edite `instalador_tuss.py`**

2. **Recompile o EXE**:
   ```bash
   compilar_exe.bat  # Windows
   ./compilar_exe.sh # Linux/Mac
   ```

3. **Distribua o novo EXE**

## 📞 Suporte

### Para problemas com a instalação
- Consulte o `GUIA_INSTALACAO.md`
- Verifique se todos os arquivos estão presentes
- Tente em outro computador

### Para problemas com os dados
- Consulte: https://www.gov.br/ans/pt-br
- Fonte: ANS - Agência Nacional de Saúde Suplementar

## 📄 Informações Legais

- **Desenvolvido por**: Manus
- **Versão**: 1.0
- **Data**: 15/03/2026
- **Licença**: Consulte a fonte original (ANS)
- **Dados**: Rol RN 465/2021 (ANS)

## ✅ Checklist de Distribuição

- [ ] EXE foi compilado com sucesso
- [ ] EXE tem 7.3 MB de tamanho
- [ ] EXE executa sem erros
- [ ] Instalação funciona corretamente
- [ ] Tabela abre no navegador
- [ ] Dados aparecem corretamente
- [ ] Atalho foi criado na Área de Trabalho
- [ ] Documentação está incluída

---

**Pronto para distribuição!** 🎉

Você pode agora compartilhar o EXE com qualquer pessoa que tenha Windows.
