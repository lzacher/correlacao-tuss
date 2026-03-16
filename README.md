# 📋 Correlação TUSS - Tabela Interativa v1.0

Tabela de Correlação entre Terminologia de Procedimentos e Eventos em Saúde e o Rol de Procedimentos e Eventos em Saúde RN nº 465/2021 e suas alterações.

## 🎯 O que é?

A **Correlação TUSS** é uma aplicação web interativa que permite buscar, filtrar e visualizar a correlação entre os códigos TUSS (Tabela de Terminologia de Procedimentos e Eventos em Saúde) e o Rol de Procedimentos da ANS.

**Características principais:**
- ✅ 6.735 procedimentos e eventos em saúde
- ✅ Busca em tempo real
- ✅ Filtros por correlação (SIM/NÃO)
- ✅ Ordenação por coluna
- ✅ Indicadores de cobertura (OD, AMB, HCO, HSO, PAC, DUT)
- ✅ Painel de estatísticas
- ✅ Design responsivo (funciona em celulares e tablets)
- ✅ Funciona completamente offline

## 🚀 Instalação Rápida

### Windows
```bash
python instalador_tuss.py
```

### Linux / macOS
```bash
chmod +x instalar_tuss.sh
./instalar_tuss.sh
```

### Instalação Manual
1. Copie `CorrelacaoTUSS_Interativa.html` para uma pasta
2. Clique duas vezes para abrir no navegador

## 📖 Documentação

Para instruções detalhadas de instalação, consulte: **[GUIA_INSTALACAO.md](GUIA_INSTALACAO.md)**

## 📦 Arquivos Inclusos

| Arquivo | Descrição |
|---------|-----------|
| `CorrelacaoTUSS_Interativa.html` | Tabela interativa (arquivo principal) |
| `CorrelacaoTUSS_2025.json` | Dados em formato JSON |
| `instalador_tuss.py` | Instalador automático para Windows |
| `instalar_tuss.sh` | Instalador automático para Linux/Mac |
| `GUIA_INSTALACAO.md` | Guia completo de instalação |
| `README.md` | Este arquivo |

## 🖥️ Requisitos

- **Navegador web**: Chrome, Firefox, Safari, Edge (versão recente)
- **Espaço em disco**: ~5 MB
- **Conexão de internet**: Não é necessária
- **Sistemas operacionais**: Windows, macOS, Linux

## 🎨 Como Usar

### Abrir a Tabela
1. Abra o arquivo `CorrelacaoTUSS_Interativa.html` em seu navegador
2. A tabela carregará com todos os registros

### Buscar Procedimentos
- Digite na barra de pesquisa para buscar por código, terminologia ou descrição

### Filtrar Resultados
- **Todos**: Exibe todos os 6.735 registros
- **Com Correlação**: Mostra apenas procedimentos com correlação (SIM)
- **Sem Correlação**: Mostra apenas procedimentos sem correlação (NÃO)

### Ordenar Dados
- Clique em qualquer cabeçalho de coluna para ordenar
- Clique novamente para inverter a ordem

### Limpar Pesquisa
- Clique no botão "✕ Limpar" para remover a busca

## 📊 Indicadores de Cobertura

| Sigla | Significado |
|-------|-------------|
| **OD** | Odontologia |
| **AMB** | Ambulatorial |
| **HCO** | Hospital com Cirurgia |
| **HSO** | Hospital sem Cirurgia |
| **PAC** | Pronto Atendimento/Clínica |
| **DUT** | Diária UTI |

## 🔍 Exemplo de Uso

1. **Buscar um procedimento específico**
   - Digite "consulta" na barra de pesquisa
   - Veja todos os procedimentos relacionados a consulta

2. **Filtrar por correlação**
   - Clique em "Com Correlação" para ver apenas procedimentos correlacionados
   - Clique em "Sem Correlação" para ver procedimentos não correlacionados

3. **Ordenar por código**
   - Clique no cabeçalho "Código"
   - Os registros serão ordenados numericamente

4. **Visualizar cobertura**
   - Veja os indicadores de cobertura em cada linha
   - Identifique quais tipos de atendimento cobrem cada procedimento

## 🌐 Compatibilidade

| Navegador | Versão Mínima | Status |
|-----------|---------------|--------|
| Chrome | 60+ | ✅ Suportado |
| Firefox | 55+ | ✅ Suportado |
| Safari | 11+ | ✅ Suportado |
| Edge | 79+ | ✅ Suportado |
| Internet Explorer | - | ❌ Não suportado |

## 📞 Informações

**Fonte**: ANS - Agência Nacional de Saúde Suplementar  
**Data de Publicação**: 17/02/2025  
**Total de Registros**: 6.735  
**Versão**: 1.0

Para mais informações sobre os dados, visite: https://www.gov.br/ans/pt-br

## 🔒 Privacidade e Segurança

- ✅ Funciona completamente offline
- ✅ Nenhum dado é enviado para servidores
- ✅ Todos os dados são armazenados localmente
- ✅ Sem rastreamento ou coleta de informações

## 📝 Notas

- A tabela funciona em qualquer navegador moderno
- Você pode copiar a pasta de instalação para outro computador
- Os dados são atualizados conforme novas resoluções da ANS
- A aplicação não requer instalação de software adicional

## 🆘 Solução de Problemas

### A tabela não abre
- Certifique-se de que seu navegador é moderno
- Tente abrir em outro navegador
- Verifique se o arquivo HTML está íntegro

### Os dados não aparecem
- Certifique-se de que o arquivo `CorrelacaoTUSS_2025.json` está na mesma pasta
- Recarregue a página (F5 ou Cmd+R)

### Busca não funciona
- Verifique se JavaScript está habilitado no navegador
- Tente limpar o cache do navegador

Para mais ajuda, consulte o **[GUIA_INSTALACAO.md](GUIA_INSTALACAO.md)**

## 📄 Licença

Esta tabela é fornecida pela ANS - Agência Nacional de Saúde Suplementar.  
Consulte a fonte original para informações sobre licença e uso.

---

**Desenvolvido por**: Manus  
**Versão**: 1.0  
**Última atualização**: 15/03/2026

Aproveite! 🎉
