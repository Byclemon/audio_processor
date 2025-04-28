@echo off
title 音频批量处理工具

:: 检查是否存在虚拟环境
if not exist venv (
    echo 创建虚拟环境...
    python -m venv venv
    echo 虚拟环境已创建。
)

:: 激活虚拟环境
call venv\Scripts\activate

:: 安装依赖
echo 安装依赖...
pip install -r requirements.txt

:: 提示用户选择运行模式
echo 音频批量处理工具
echo ====================
echo 请选择运行模式:
echo 1. 命令行模式
echo 2. 图形界面模式
echo 3. 退出
set /p choice=请输入选项 [1-3]: 

if "%choice%"=="1" (
    :: 命令行模式
    echo 启动命令行模式...
    set /p input_dir=输入目录: 
    set /p output_dir=输出目录: 
    set /p min_duration=最小时长(秒) [默认15]: 
    
    :: 设置默认值
    if "%min_duration%"=="" set min_duration=15
    
    :: 运行命令行模式
    python main.py -i "%input_dir%" -o "%output_dir%" -d %min_duration%
) else if "%choice%"=="2" (
    :: 图形界面模式
    echo 启动图形界面模式...
    python gui_main.py
) else if "%choice%"=="3" (
    echo 退出程序
) else (
    echo 无效选项，退出程序
)

:: 停用虚拟环境
call venv\Scripts\deactivate
pause 