#!/usr/bin/env python3
"""
打包脚本 - 使用PyInstaller将应用打包成可执行文件
"""
import PyInstaller.__main__
import os
import sys

# 确保在正确的目录中
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 图标路径
icon = os.path.join('assets', 'app_icon.png')

# 如果图标不存在，尝试生成它
if not os.path.exists(icon):
    try:
        import create_icon
        icon = create_icon.create_icon()
    except:
        print("无法创建图标，将使用默认图标")
        icon = None

# 应用名称
app_name = "音频批量处理工具"

# 打包参数
params = [
    'gui_main.py',                  # 主脚本
    '--name=%s' % app_name,         # 应用名称
    '--windowed',                  # 使用窗口（GUI）模式，不显示控制台
    '--add-data=requirements.txt:.',  # 添加数据文件
    '--add-data=assets:assets',    # 添加资源文件（包括图标）
    '--collect-submodules=src',    # 确保收集src模块
    '--noconfirm',                 # 不询问确认
    '--clean',                     # 清理临时文件
    '--log-level=INFO',            # 日志级别
]

# 添加图标（如果有）
if icon and os.path.exists(icon):
    params.append('--icon=%s' % icon)
    print(f"使用图标: {icon}")

# 启动PyInstaller
PyInstaller.__main__.run(params)

print("打包完成！可执行文件位于 dist 目录中。") 