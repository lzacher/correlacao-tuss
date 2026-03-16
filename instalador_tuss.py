#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador da Tabela de Correlação TUSS
Versão 1.0
Autor: Manus
Descrição: Instala a tabela HTML interativa de correlação TUSS em qualquer computador
"""

import os
import sys
import shutil
import json
import webbrowser
from pathlib import Path
from datetime import datetime

class InstaladorTUSS:
    def __init__(self):
        self.nome_app = "Correlação TUSS"
        self.versao = "1.0"
        self.nome_arquivo = "CorrelacaoTUSS_Interativa.html"
        self.arquivo_json = "CorrelacaoTUSS_2025.json"
        
    def limpar_tela(self):
        """Limpa a tela do console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self):
        """Exibe o cabeçalho do instalador"""
        self.limpar_tela()
        print("=" * 70)
        print(f"  {self.nome_app} - Instalador v{self.versao}")
        print("=" * 70)
        print()
        print("  Tabela de Correlação entre Terminologia de Procedimentos")
        print("  e Eventos em Saúde - Rol RN 465/2021")
        print()
        print("  Publicado em 17/02/2025")
        print("  ANS - Agência Nacional de Saúde Suplementar")
        print()
        print("=" * 70)
        print()
    
    def obter_caminho_instalacao(self):
        """Obtém o caminho de instalação do usuário"""
        print("📁 SELEÇÃO DO DIRETÓRIO DE INSTALAÇÃO")
        print("-" * 70)
        print()
        
        # Sugerir caminho padrão
        if os.name == 'nt':  # Windows
            caminho_padrao = os.path.join(os.path.expanduser("~"), "Desktop", "Correlação TUSS")
        else:  # Linux/Mac
            caminho_padrao = os.path.join(os.path.expanduser("~"), "Documentos", "Correlação TUSS")
        
        print(f"Caminho padrão sugerido:")
        print(f"  {caminho_padrao}")
        print()
        
        while True:
            resposta = input("Deseja instalar neste local? (S/n): ").strip().lower()
            
            if resposta in ['s', '']:
                caminho = caminho_padrao
                break
            elif resposta == 'n':
                caminho = input("\nDigite o caminho completo desejado: ").strip()
                if not caminho:
                    print("❌ Caminho inválido!")
                    continue
                break
            else:
                print("❌ Opção inválida! Digite 'S' ou 'n'")
                continue
        
        return caminho
    
    def criar_diretorio(self, caminho):
        """Cria o diretório de instalação"""
        try:
            Path(caminho).mkdir(parents=True, exist_ok=True)
            print(f"✓ Diretório criado: {caminho}")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar diretório: {e}")
            return False
    
    def copiar_arquivo_html(self, caminho_origem, caminho_destino):
        """Copia o arquivo HTML para o diretório de instalação"""
        try:
            arquivo_destino = os.path.join(caminho_destino, self.nome_arquivo)
            shutil.copy2(caminho_origem, arquivo_destino)
            print(f"✓ Arquivo HTML instalado: {arquivo_destino}")
            return arquivo_destino
        except Exception as e:
            print(f"❌ Erro ao copiar arquivo HTML: {e}")
            return None
    
    def copiar_arquivo_json(self, caminho_origem, caminho_destino):
        """Copia o arquivo JSON para o diretório de instalação"""
        try:
            arquivo_destino = os.path.join(caminho_destino, self.arquivo_json)
            shutil.copy2(caminho_origem, arquivo_destino)
            print(f"✓ Arquivo JSON instalado: {arquivo_destino}")
            return arquivo_destino
        except Exception as e:
            print(f"❌ Erro ao copiar arquivo JSON: {e}")
            return None
    
    def criar_atalho_desktop(self, caminho_html, caminho_destino):
        """Cria um atalho na área de trabalho (Windows)"""
        if os.name != 'nt':
            return True
        
        try:
            import win32com.client
            
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            atalho_path = os.path.join(desktop, f"{self.nome_app}.lnk")
            
            shell = win32com.client.Dispatch("WScript.Shell")
            atalho = shell.CreateShortCut(atalho_path)
            atalho.TargetPath = caminho_html
            atalho.WorkingDirectory = caminho_destino
            atalho.IconLocation = caminho_html
            atalho.save()
            
            print(f"✓ Atalho criado na área de trabalho")
            return True
        except Exception as e:
            print(f"⚠ Aviso: Não foi possível criar atalho na área de trabalho ({e})")
            return True  # Não é crítico
    
    def criar_arquivo_info(self, caminho_destino):
        """Cria um arquivo de informações sobre a instalação"""
        try:
            info = {
                "nome_app": self.nome_app,
                "versao": self.versao,
                "data_instalacao": datetime.now().isoformat(),
                "arquivo_principal": self.nome_arquivo,
                "arquivo_dados": self.arquivo_json,
                "descricao": "Tabela de Correlação TUSS - Rol RN 465/2021",
                "total_registros": 6735,
                "fonte": "ANS - Agência Nacional de Saúde Suplementar",
                "data_publicacao": "17/02/2025"
            }
            
            arquivo_info = os.path.join(caminho_destino, "INFO.json")
            with open(arquivo_info, 'w', encoding='utf-8') as f:
                json.dump(info, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Arquivo de informações criado")
            return True
        except Exception as e:
            print(f"⚠ Aviso: Não foi possível criar arquivo de informações ({e})")
            return True
    
    def criar_arquivo_leiame(self, caminho_destino):
        """Cria um arquivo README com instruções"""
        try:
            readme_content = f"""# {self.nome_app} v{self.versao}

## Descrição
Tabela de Correlação entre Terminologia de Procedimentos e Eventos em Saúde
e o Rol de Procedimentos e Eventos em Saúde RN nº 465/2021 e suas alterações.

## Arquivos Inclusos
- **{self.nome_arquivo}**: Tabela interativa (abrir no navegador)
- **{self.arquivo_json}**: Dados em formato JSON
- **INFO.json**: Informações sobre a instalação
- **LEIAME.txt**: Este arquivo

## Como Usar
1. Abra o arquivo "{self.nome_arquivo}" em qualquer navegador web
2. Use a barra de pesquisa para buscar procedimentos
3. Clique nos cabeçalhos para ordenar os dados
4. Use os filtros para refinar os resultados

## Funcionalidades
✓ Busca em tempo real
✓ Filtros por correlação (SIM/NÃO)
✓ Ordenação por coluna
✓ Indicadores de cobertura (OD, AMB, HCO, HSO, PAC, DUT)
✓ Painel de estatísticas
✓ Design responsivo (funciona em celulares e tablets)

## Requisitos
- Navegador web moderno (Chrome, Firefox, Edge, Safari)
- Sem necessidade de conexão com a internet

## Fonte
ANS - Agência Nacional de Saúde Suplementar
Publicado em: 17/02/2025

## Suporte
Para dúvidas sobre os dados, consulte:
https://www.gov.br/ans/pt-br

---
Instalado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}
"""
            
            arquivo_readme = os.path.join(caminho_destino, "LEIAME.txt")
            with open(arquivo_readme, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"✓ Arquivo LEIAME.txt criado")
            return True
        except Exception as e:
            print(f"⚠ Aviso: Não foi possível criar arquivo LEIAME.txt ({e})")
            return True
    
    def instalar(self):
        """Executa o processo de instalação"""
        self.exibir_cabecalho()
        
        # Encontrar arquivos de origem
        script_dir = os.path.dirname(os.path.abspath(__file__))
        arquivo_html_origem = os.path.join(script_dir, self.nome_arquivo)
        arquivo_json_origem = os.path.join(script_dir, self.arquivo_json)
        
        # Verificar se os arquivos existem
        if not os.path.exists(arquivo_html_origem):
            print(f"❌ ERRO: Arquivo '{self.nome_arquivo}' não encontrado!")
            print(f"   Procurado em: {arquivo_html_origem}")
            input("\nPressione ENTER para sair...")
            return False
        
        if not os.path.exists(arquivo_json_origem):
            print(f"⚠ AVISO: Arquivo '{self.arquivo_json}' não encontrado!")
            print(f"   A tabela funcionará, mas sem os dados atualizados")
        
        # Obter caminho de instalação
        caminho_instalacao = self.obter_caminho_instalacao()
        
        print()
        print("📦 INICIANDO INSTALAÇÃO")
        print("-" * 70)
        print()
        
        # Criar diretório
        if not self.criar_diretorio(caminho_instalacao):
            input("\nPressione ENTER para sair...")
            return False
        
        # Copiar arquivos
        arquivo_html_instalado = self.copiar_arquivo_html(arquivo_html_origem, caminho_instalacao)
        if not arquivo_html_instalado:
            input("\nPressione ENTER para sair...")
            return False
        
        if os.path.exists(arquivo_json_origem):
            self.copiar_arquivo_json(arquivo_json_origem, caminho_instalacao)
        
        # Criar arquivos adicionais
        self.criar_arquivo_info(caminho_instalacao)
        self.criar_arquivo_leiame(caminho_instalacao)
        
        # Criar atalho (Windows)
        if os.name == 'nt':
            self.criar_atalho_desktop(arquivo_html_instalado, caminho_instalacao)
        
        # Sucesso
        print()
        print("=" * 70)
        print("✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print()
        print(f"Local de instalação: {caminho_instalacao}")
        print()
        
        # Perguntar se deseja abrir
        print("Deseja abrir a tabela agora? (S/n): ", end="")
        resposta = input().strip().lower()
        
        if resposta in ['s', '']:
            try:
                webbrowser.open('file://' + arquivo_html_instalado)
                print("✓ Abrindo no navegador...")
            except Exception as e:
                print(f"⚠ Não foi possível abrir automaticamente: {e}")
                print(f"  Abra manualmente: {arquivo_html_instalado}")
        
        print()
        input("Pressione ENTER para sair...")
        return True

def main():
    """Função principal"""
    try:
        instalador = InstaladorTUSS()
        sucesso = instalador.instalar()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Instalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("\nPressione ENTER para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()
