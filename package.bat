@echo off
title 音频批量处理工具 - 打包

:: 确保在项目目录
cd /d "%~dp0"

:: 创建虚拟环境（如果不存在）
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
)

:: 激活虚拟环境
call venv\Scripts\activate

:: 安装依赖
echo 安装依赖...
pip install -r requirements.txt
pip install pyinstaller

:: 打包应用
echo 开始打包应用...
pyinstaller --name="音频批量处理工具" --onefile --windowed --noconfirm gui_main.py

echo 打包完成！应用位于 dist 目录。

:: 清理
call venv\Scripts\deactivate
pause 