#!/bin/bash

# 音频批量处理工具启动脚本

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "Installing dependencies..."
pip install -r requirements.txt

# 提示用户选择运行模式
echo "音频批量处理工具"
echo "===================="
echo "请选择运行模式:"
echo "1. 命令行模式"
echo "2. 图形界面模式"
echo "3. 退出"
read -p "请输入选项 [1-3]: " choice

case $choice in
    1)  # 命令行模式
        echo "启动命令行模式..."
        read -p "输入目录: " input_dir
        read -p "输出目录: " output_dir
        read -p "最小时长(秒) [默认15]: " min_duration
        
        # 设置默认值
        min_duration=${min_duration:-15}
        
        # 运行命令行模式
        python main.py -i "$input_dir" -o "$output_dir" -d "$min_duration"
        ;;
    2)  # 图形界面模式
        echo "启动图形界面模式..."
        python gui_main.py
        ;;
    3)  # 退出
        echo "退出程序"
        ;;
    *)  # 无效选项
        echo "无效选项，退出程序"
        ;;
esac

# 停用虚拟环境
deactivate 