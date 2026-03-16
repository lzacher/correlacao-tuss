@echo off
REM ============================================================================
REM Script para compilar o instalador TUSS para EXE no Windows
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo  Compilador de EXE - Correlacao TUSS
echo ============================================================================
echo.

REM Verificar se Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.6 ou superior de:
    echo   https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [1/4] Verificando Python...
python --version

echo.
echo [2/4] Instalando PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERRO: Falha ao instalar PyInstaller
    pause
    exit /b 1
)

echo.
echo [3/4] Compilando instalador para EXE...
echo Isso pode levar alguns minutos...
echo.

pyinstaller --onefile ^
    --windowed ^
    --name "Instalador Correlacao TUSS" ^
    --add-data "CorrelacaoTUSS_Interativa.html;." ^
    --add-data "CorrelacaoTUSS_2025.json;." ^
    --distpath ".\dist" ^
    --workpath ".\build" ^
    --specpath ".\spec" ^
    instalador_tuss.py

if errorlevel 1 (
    echo.
    echo ERRO: Falha na compilacao
    pause
    exit /b 1
)

echo.
echo [4/4] Finalizando...
echo.

REM Verificar se o EXE foi criado
if exist "dist\Instalador Correlacao TUSS.exe" (
    echo ============================================================================
    echo SUCESSO! EXE criado com sucesso!
    echo ============================================================================
    echo.
    echo Arquivo gerado: dist\Instalador Correlacao TUSS.exe
    echo Tamanho: 
    for %%A in ("dist\Instalador Correlacao TUSS.exe") do echo   %%~zA bytes
    echo.
    echo Voce pode agora distribuir este arquivo junto com:
    echo   - CorrelacaoTUSS_Interativa.html
    echo   - CorrelacaoTUSS_2025.json
    echo.
    echo Ou copiar apenas o EXE para a pasta "dist" e distribuir tudo junto.
    echo.
) else (
    echo ERRO: EXE nao foi criado
    pause
    exit /b 1
)

pause
