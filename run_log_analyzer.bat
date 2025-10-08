@echo off
echo -------------------------------
echo Start checking and install dependencies...
echo -------------------------------

REM 虚拟环境路径
set VENV_PATH=venv

REM 激活虚拟环境
call "%VENV_PATH%\Scripts\activate.bat"

REM 安装依赖
pip install --upgrade pip
pip install pyyaml

echo -------------------------------
echo Dependencies OK, start log analyzer
echo -------------------------------

pip install pyyaml

echo [Run] Starting multi-color log analyzer...
python log_analyzer.py

pause
