#!/usr/bin/env python3
"""
DMG打包脚本 - 将.app应用打包成DMG格式
"""
import os
import subprocess
import sys
import shutil
from datetime import datetime

def build_dmg():
    # 确保在正确的目录中
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 应用名称
    app_name = "音频批量处理工具"
    app_path = os.path.join("dist", f"{app_name}.app")
    
    # 检查.app文件是否存在
    if not os.path.exists(app_path):
        print(f"错误：未找到应用程序 {app_path}")
        print("请先运行 build_app.py 生成应用程序")
        return False
    
    # DMG文件名（带版本日期）
    current_date = datetime.now().strftime("%Y%m%d")
    dmg_name = f"{app_name}_v{current_date}"
    dmg_path = os.path.join("dist", f"{dmg_name}.dmg")
    
    # 创建临时DMG目录
    temp_dir = os.path.join("dist", "dmg_temp")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
    
    # 复制.app到临时目录
    temp_app_path = os.path.join(temp_dir, f"{app_name}.app")
    print(f"复制应用到临时目录: {temp_app_path}")
    shutil.copytree(app_path, temp_app_path)
    
    # 创建应用程序快捷方式
    os.symlink("/Applications", os.path.join(temp_dir, "Applications"))
    
    # 创建DMG
    print(f"创建DMG: {dmg_path}")
    
    # 删除已存在的DMG
    if os.path.exists(dmg_path):
        os.remove(dmg_path)
    
    # 基本DMG创建命令
    cmd = [
        "hdiutil", "create",
        "-volname", app_name,
        "-srcfolder", temp_dir,
        "-ov", "-format", "UDZO",
        dmg_path
    ]
    
    # 执行命令
    try:
        subprocess.run(cmd, check=True)
        print(f"DMG创建成功：{dmg_path}")
        
        # 清理
        shutil.rmtree(temp_dir)
        return True
    except subprocess.CalledProcessError as e:
        print(f"创建DMG时出错: {e}")
        return False

if __name__ == "__main__":
    if build_dmg():
        print("DMG打包完成！")
    else:
        print("DMG打包失败！")
        sys.exit(1)