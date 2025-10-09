@echo off
REM =========================
REM Windows: 构建本地日志分析器 EXE
REM =========================

REM 进入项目目录
cd /d %~dp0

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 更新 pip
python -m pip install --upgrade pip

REM 安装打包工具 PyInstaller
pip install pyinstaller --upgrade

REM 删除旧的打包文件
rmdir /s /q dist
rmdir /s /q build
del /q log_analyzer.spec

REM 生成单文件 EXE
pyinstaller --noconsole --onefile log_analyzer.py

REM 提示完成
echo.
echo ===============================
echo Build complete!
echo EXE located in: dist\log_analyzer.exe
echo ===============================
pause
