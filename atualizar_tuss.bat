@echo off
REM =============================================================================
REM Wrapper de Atualização TUSS para Windows
REM Verifica dependências e executa o script Python principal
REM
REM Uso:
REM   atualizar_tuss.bat --arquivo novo_tuss.xlsx
REM   atualizar_tuss.bat --arquivo novo_tuss.xlsx --versao 2026.01
REM   atualizar_tuss.bat --verificar
REM =============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo   Atualizacao Automatica - Correlacao TUSS
echo ============================================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Instale Python 3.6 ou superior em: https://www.python.org/downloads/
    echo Marque a opcao "Add Python to PATH" durante a instalacao.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo [OK] %%v

REM Verificar dependências Python
echo [INFO] Verificando dependencias Python...
python -c "import pandas, openpyxl" >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Instalando dependencias necessarias...
    pip install pandas openpyxl --quiet
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas
) else (
    echo [OK] Dependencias OK
)

REM Verificar Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Git nao encontrado. Push para GitHub nao sera possivel.
    echo         Instale em: https://git-scm.com/download/win
) else (
    for /f "tokens=*" %%v in ('git --version 2^>^&1') do echo [OK] %%v
)

echo.

REM Executar script Python com todos os argumentos
python "%~dp0atualizar_tuss.py" %*

if errorlevel 1 (
    echo.
    echo [ERRO] Atualizacao falhou. Verifique as mensagens acima.
    pause
    exit /b 1
)

pause
