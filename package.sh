#!/bin/bash

# 确保在项目目录
cd "$(dirname "$0")"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装依赖..."
pip install -r requirements.txt
pip install pyinstaller

# 打包应用
echo "开始打包应用..."
# 使用build_app.py进行打包，而不是直接调用pyinstaller
python build_app.py

echo "打包完成！应用位于 dist 目录。"

# 清理
deactivate 