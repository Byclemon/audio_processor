import sys
import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
import threading
import logging
import webbrowser
from pathlib import Path
from .audio_processor import AudioProcessor

class RedirectText:
    """重定向文本到Tkinter Text控件"""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, string):
        self.buffer += string
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def flush(self):
        pass

class TkTextHandler(logging.Handler):
    """将日志输出到Tkinter文本框的处理器"""
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

class AboutDialog(tk.Toplevel):
    """关于和赞助对话框"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("关于音频批量处理工具")
        self.geometry("600x500")  # 增大对话框初始尺寸
        self.minsize(500, 400)  # 增大最小尺寸
        self.transient(parent)  # 设置为父窗口的临时窗口
        self.grab_set()  # 模态窗口
        
        # 创建选项卡
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 赞助页面 - 放在第一位
        donate_frame = ttk.Frame(notebook, padding=10)
        notebook.add(donate_frame, text="赞助支持")
        
        # 使用说明页面 - 放在第二位
        help_frame = ttk.Frame(notebook, padding=10)
        notebook.add(help_frame, text="使用说明")
        
        # 关于页面 - 放在第三位
        about_frame = ttk.Frame(notebook, padding=10)
        notebook.add(about_frame, text="关于")
        
        # 关于页面内容
        ttk.Label(about_frame, text="音频批量处理工具", font=("Helvetica", 16)).pack(pady=10)
        ttk.Label(about_frame, text="版本：1.0.0").pack()
        ttk.Label(about_frame, text="一款简单易用的音频批量处理工具，\n可将短音频拼接成较长音频文件").pack(pady=10)
        ttk.Label(about_frame, text="联系方式：byclemon").pack(pady=5)
        ttk.Label(about_frame, text="© 2025 版权所有").pack(pady=5)
        
        # 使用说明页面内容
        help_text = tk.Text(help_frame, wrap=tk.WORD, height=15)
        help_text.pack(fill=tk.BOTH, expand=True)
        help_scroll = ttk.Scrollbar(help_frame, command=help_text.yview)
        help_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        help_text.config(yscrollcommand=help_scroll.set)
        
        help_content = """使用说明：

1. 选择输入目录：点击"浏览..."按钮选择包含多个短音频文件的文件夹。

2. 选择输出目录：点击"浏览..."按钮选择合并后的音频文件的保存位置。

3. 设置最小时长：设置合并后音频文件的最小时长（秒）。

4. 点击"开始处理"：程序将自动读取输入目录中的所有音频文件，并按照从短到长的顺序进行排序和合并。

5. 处理过程：处理过程中可以在日志区域查看进度。

6. 完成：处理完成后，合并后的音频文件将保存在指定的输出目录中。

支持的音频格式：MP3、WAV、FLAC、OGG、M4A、AAC

注意事项：
- 确保输入目录中包含支持的音频文件格式
- 程序会自动创建输出目录（如果不存在）
- 合并过程中不会修改原始音频文件
        """
        
        help_text.insert(tk.END, help_content)
        help_text.config(state=tk.DISABLED)
        
        # 赞助页面内容
        ttk.Label(donate_frame, text="感谢您的支持！", font=("Helvetica", 14)).pack(pady=10)
        ttk.Label(donate_frame, text="如果您觉得这个工具有用，可以考虑赞助开发者，\n这将帮助我们持续改进此工具。").pack(pady=10)
        
        # 显示赞助图片（从assets目录直接加载用户提供的图片）
        try:
            # 获取assets目录路径
            assets_dir = Path(__file__).parent.parent / "assets"
            
            # 尝试加载常见的图片名称
            image_names = ["logo.png", "donate.png", "wechat.png", "alipay.png", "sponsor.png"]
            image_path = None
            
            # 查找第一个存在的图片
            for name in image_names:
                path = assets_dir / name
                if path.exists():
                    image_path = path
                    break
            
            # 如果找到图片，显示它
            if image_path:
                from PIL import Image, ImageTk
                
                # 加载并显示图片
                img = Image.open(image_path)
                
                # 调整图片大小，最大宽度和高度更小
                max_size = 250  # 设置较小的尺寸
                width, height = img.size
                if width > height:
                    # 如果宽度大于高度，以宽度为基准缩放
                    ratio = max_size / width
                    new_height = int(height * ratio)
                    img = img.resize((max_size, new_height), Image.LANCZOS)
                else:
                    # 如果高度大于或等于宽度，以高度为基准缩放
                    ratio = max_size / height
                    new_width = int(width * ratio)
                    img = img.resize((new_width, max_size), Image.LANCZOS)
                
                photo = ImageTk.PhotoImage(img)
                
                # 直接在捐赠框架中显示图片，不使用滚动功能
                label = ttk.Label(donate_frame, image=photo)
                label.image = photo  # 保持引用以防止垃圾回收
                label.pack(pady=10)
            else:
                ttk.Label(donate_frame, text="请在assets目录中放入您的赞助二维码图片").pack(pady=10)
        except Exception as e:
            ttk.Label(donate_frame, text=f"加载图片时出错: {str(e)}").pack(pady=10)
            ttk.Label(donate_frame, text="请确保assets目录中有您的赞助图片").pack()
        
        # 添加项目主页链接
        ttk.Label(donate_frame, text="访问项目主页了解更多：").pack(pady=10)
        project_link = ttk.Label(donate_frame, text="https://github.com/yourusername/audio-processor", 
                                foreground="blue", cursor="hand2")
        project_link.pack()
        project_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/yourusername/audio-processor"))
        
        # 确定按钮
        ttk.Button(self, text="确定", command=self.destroy).pack(pady=10)
        
        # 居中显示
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (parent.winfo_width() - width) // 2 + parent.winfo_x()
        y = (parent.winfo_height() - height) // 2 + parent.winfo_y()
        self.geometry(f"{width}x{height}+{x}+{y}")

class AudioProcessorGUI:
    """音频处理器的图形用户界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("音频批量处理工具")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        # 创建GUI组件
        self.create_widgets()
        
        # 设置日志
        self.logger = logging.getLogger('AudioProcessor')
        self.logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别，显示更详细的日志
        
        # 添加日志处理器，将日志输出到文本框
        self.text_handler = TkTextHandler(self.log_text)
        self.text_handler.setLevel(logging.DEBUG)
        self.text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.text_handler)
        
        # 处理中标志
        self.processing = False
    
    def create_widgets(self):
        """创建GUI组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 输入路径选择
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="输入目录:").pack(side=tk.LEFT)
        self.input_path_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.input_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(input_frame, text="浏览...", command=self.browse_input_dir).pack(side=tk.LEFT)
        
        # 输出路径选择
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_path_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(output_frame, text="浏览...", command=self.browse_output_dir).pack(side=tk.LEFT)
        
        # 最小时长设置
        duration_frame = ttk.Frame(main_frame)
        duration_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(duration_frame, text="最小时长(秒):").pack(side=tk.LEFT)
        self.min_duration_var = tk.DoubleVar(value=15.0)
        ttk.Spinbox(duration_frame, from_=1.0, to=3600.0, increment=1.0, 
                   textvariable=self.min_duration_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # 处理按钮和说明/赞助按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="开始处理", command=self.start_processing, width=15)
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        # 添加说明/赞助按钮
        self.about_button = ttk.Button(button_frame, text="说明/赞助", command=self.show_about_dialog, width=15)
        self.about_button.pack(side=tk.LEFT, padx=5)
        
        # 日志文本框
        log_frame = ttk.LabelFrame(main_frame, text="处理日志")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, height=10)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)
        
        # 重定向stdout到日志文本框
        self.stdout_redirect = RedirectText(self.log_text)
        sys.stdout = self.stdout_redirect
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def browse_input_dir(self):
        """浏览选择输入目录"""
        directory = filedialog.askdirectory(title="选择输入音频目录")
        if directory:
            self.input_path_var.set(directory)
    
    def browse_output_dir(self):
        """浏览选择输出目录"""
        directory = filedialog.askdirectory(title="选择输出音频目录")
        if directory:
            self.output_path_var.set(directory)
    
    def show_about_dialog(self):
        """显示关于和赞助对话框"""
        AboutDialog(self.root)
    
    def start_processing(self):
        """开始处理音频文件"""
        if self.processing:
            messagebox.showinfo("提示", "处理正在进行中，请等待完成")
            return
        
        input_dir = self.input_path_var.get().strip()
        output_dir = self.output_path_var.get().strip()
        min_duration = self.min_duration_var.get()
        
        # 验证输入
        if not input_dir:
            messagebox.showerror("错误", "请选择输入目录")
            return
        
        if not output_dir:
            messagebox.showerror("错误", "请选择输出目录")
            return
        
        if not os.path.exists(input_dir):
            messagebox.showerror("错误", f"输入目录不存在: {input_dir}")
            return
        
        # 清空日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 更新UI状态
        self.processing = True
        self.process_button.config(state=tk.DISABLED)
        self.status_var.set("处理中...")
        
        # 在新线程中处理
        thread = threading.Thread(target=self.process_audio_files, 
                                 args=(input_dir, output_dir, min_duration))
        thread.daemon = True
        thread.start()
    
    def process_audio_files(self, input_dir, output_dir, min_duration):
        """在后台线程中处理音频文件"""
        try:
            # 创建处理器
            processor = AudioProcessor(
                input_dir=input_dir,
                output_dir=output_dir,
                min_duration_ms=int(min_duration * 1000)
            )
            
            # 开始处理
            self.logger.info("开始处理音频文件...")
            count = processor.process()
            
            if count > 0:
                self.logger.info(f"处理完成: 成功生成 {count} 个音频文件")
                self.logger.info(f"输出目录: {output_dir}")
                messagebox.showinfo("成功", f"处理完成: 成功生成 {count} 个音频文件")
            else:
                self.logger.warning("未生成任何音频文件，请检查输入文件夹是否包含支持的音频文件")
                messagebox.showwarning("警告", "未生成任何音频文件，请检查输入文件夹是否包含支持的音频文件")
                
        except Exception as e:
            self.logger.error(f"处理过程中出错: {str(e)}")
            messagebox.showerror("错误", f"处理过程中出错: {str(e)}")
        
        finally:
            # 恢复UI状态
            self.root.after(0, self.reset_ui)
    
    def reset_ui(self):
        """重置UI状态"""
        self.processing = False
        self.process_button.config(state=tk.NORMAL)
        self.status_var.set("就绪")

def main():
    """GUI主函数"""
    root = tk.Tk()
    app = AudioProcessorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 