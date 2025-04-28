#!/usr/bin/env python3
"""
音频批量处理工具图形界面入口脚本
"""
import tkinter as tk
from src.gui import AudioProcessorGUI

def main():
    root = tk.Tk()
    app = AudioProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 