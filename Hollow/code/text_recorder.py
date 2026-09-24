import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os

class TextInputApp:
    def __init__(self, root):
        self.root = root
        # 设置窗口标题为空字符串，只保留控制按钮
        self.root.title("")
        
        # 设置窗口大小
        window_width = 300
        window_height = 130
        self.root.geometry(f"{window_width}x{window_height}")
        
        # 将窗口定位到桌面右下角
        # 获取屏幕宽度和高度
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # 计算窗口位置
        x = screen_width - window_width
        y = screen_height - window_height
        # 设置窗口位置
        self.root.geometry(f"+{x}+{y}")
        
        self.root.resizable(True, True)
        # 设置窗口透明度，0.0-1.0，越小越透明
        self.root.attributes('-alpha', 0.2)
        
        # 设置窗口样式
        self.setup_style()
        
        # 创建界面元素
        self.create_widgets()
        
        # 绑定快捷键
        self.root.bind('<Control-Return>', self.save_text)
    
    def setup_style(self):
        # 设置CSS变量风格的颜色和字体
        self.primary_color = "#2561EF"
        self.aux_red = "#FA746B"
        self.aux_green = "#3DD4A7"
        self.neutral_dark = "#333333"
        self.neutral_medium = "#666666"
        self.neutral_light = "#999999"
        self.neutral_lighter = "#CCCCCC"
        self.background = "#FAFAF2"
        
        # 字体设置
        self.font_large = ("微软雅黑", 14, "normal")
        self.font_heading1 = ("微软雅黑", 12, "normal")
        self.font_heading2 = ("微软雅黑", 10, "normal")
        self.font_body = ("微软雅黑", 9, "normal")
        self.font_small = ("微软雅黑", 8, "normal")
        
        # 设置窗口背景
        self.root.configure(bg=self.background)
    
    def create_widgets(self):
        # 移除标题标签，不再显示"文本输入记录"文字
        
        # 文本输入框
        self.text_input = tk.Text(
            self.root,
            width=50,
            height=8,
            font=self.font_body,
            bg="white",
            fg=self.neutral_dark,
            borderwidth=2,
            relief="solid"
        )
        self.text_input.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        self.text_input.focus_set()
        
        # 确认按钮 - 已注释掉
        # self.save_button = tk.Button(
        #     self.root,
        #     text="确认保存",
        #     command=self.save_text,
        #     bg=self.primary_color,
        #     fg="white",
        #     font=self.font_heading2,
        #     padx=20,
        #     pady=10,
        #     relief="raised",
        #     borderwidth=2
        # )
        # self.save_button.pack(pady=20)
        
        # 状态标签 - 已移除，不再显示状态信息
        # self.status_label = ttk.Label(
        #     self.root,
        #     text="",
        #     font=self.font_small,
        #     foreground=self.neutral_medium,
        #     background=self.background
        # )
        # self.status_label.pack()
    
    def save_text(self, event=None):
        # 获取用户输入的文本
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            self.update_status("请输入文本内容", "error")
            return
        
        try:
            # 获取当前日期和时间
            now = datetime.now()
            year_str = now.strftime("%Y")  # 年份格式 (如2025)
            month_str = now.strftime("%m")  # 月份格式 (如01)
            day_str = now.strftime("%Y%m%d")  # 年月日格式 (如20251208)
            time_str = now.strftime("%H:%M:%S")  # 时间格式
            
            # 创建文件路径：output/年/月/日.txt
            output_dir = os.path.join(os.getcwd(), "output", year_str, month_str)
            os.makedirs(output_dir, exist_ok=True)  # 创建年和月目录（如果不存在）
            file_name = f"{day_str}.txt"
            file_path = os.path.join(output_dir, file_name)
            
            # 写入文件
            with open(file_path, "a", encoding="utf-8") as f:
                f.write(f"{time_str} - {text}\n")
            
            # 清空输入框
            self.text_input.delete(1.0, tk.END)
            self.update_status(f"内容已保存到 {file_name}", "success")
            
        except Exception as e:
            self.update_status(f"保存失败: {str(e)}", "error")
    
    def update_status(self, message, status_type):
        """更新状态标签（已移除标签，此方法不再起作用）"""
        # 状态标签已移除，不再更新状态信息
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = TextInputApp(root)
    root.mainloop()