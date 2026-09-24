import os
import shutil
import re
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class PhotoOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("照片/视频整理工具")
        self.root.geometry("600x400")
        self.root.configure(bg="#FAFAF2")
        
        self.source_dir = tk.StringVar()
        self.dest_dir = tk.StringVar()
        self.video_dest_dir = tk.StringVar()
        self.is_processing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # 移除ttk样式设置，使用标准tk.Button
        
        # 标题
        title_label = tk.Label(self.root, text="照片/视频整理工具", font=(
            "微软雅黑", 16, "bold"), bg="#FAFAF2", fg="#2561EF")
        title_label.pack(pady=10)
        
        # 源目录选择
        source_frame = tk.Frame(self.root, bg="#FAFAF2")
        source_frame.pack(pady=5, fill=tk.X, padx=50)
        
        tk.Label(source_frame, text="原始照片/视频目录:", font=("微软雅黑", 12), bg="#FAFAF2", fg="#333333").pack(anchor=tk.W)
        
        source_entry_frame = tk.Frame(source_frame, bg="#FAFAF2")
        source_entry_frame.pack(fill=tk.X, pady=3)
        
        tk.Entry(source_entry_frame, textvariable=self.source_dir, width=40, font=("微软雅黑", 10), bd=2, relief=tk.SOLID, bg="white", fg="#333333").pack(side=tk.LEFT, expand=True, fill=tk.X)
        # 浏览按钮：缩小尺寸并优化圆角效果
        browse_btn = tk.Button(source_entry_frame, text="浏览", command=self.browse_source,
                             font=('微软雅黑', 8),
                             width=6,
                             height=1,
                             bg="white",
                             fg="#333333",
                             borderwidth=1,
                             relief="ridge",
                             padx=5,
                             pady=3)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # 目标目录选择
        dest_frame = tk.Frame(self.root, bg="#FAFAF2")
        dest_frame.pack(pady=5, fill=tk.X, padx=50)
        
        tk.Label(dest_frame, text="照片备份目录:", font=("微软雅黑", 12), bg="#FAFAF2", fg="#333333").pack(anchor=tk.W)
        
        dest_entry_frame = tk.Frame(dest_frame, bg="#FAFAF2")
        dest_entry_frame.pack(fill=tk.X, pady=3)
        
        tk.Entry(dest_entry_frame, textvariable=self.dest_dir, width=40, font=("微软雅黑", 10), bd=2, relief=tk.SOLID, bg="white", fg="#333333").pack(side=tk.LEFT, expand=True, fill=tk.X)
        # 浏览按钮：缩小尺寸并优化圆角效果
        browse_btn = tk.Button(dest_entry_frame, text="浏览", command=self.browse_dest,
                             font=('微软雅黑', 8),
                             width=6,
                             height=1,
                             bg="white",
                             fg="#333333",
                             borderwidth=1,
                             relief="ridge",
                             padx=5,
                             pady=3)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # 视频备份目录选择
        video_dest_frame = tk.Frame(self.root, bg="#FAFAF2")
        video_dest_frame.pack(pady=5, fill=tk.X, padx=50)
        
        tk.Label(video_dest_frame, text="视频备份目录:", font=("微软雅黑", 12), bg="#FAFAF2", fg="#333333").pack(anchor=tk.W)
        
        video_dest_entry_frame = tk.Frame(video_dest_frame, bg="#FAFAF2")
        video_dest_entry_frame.pack(fill=tk.X, pady=3)
        
        tk.Entry(video_dest_entry_frame, textvariable=self.video_dest_dir, width=40, font=("微软雅黑", 10), bd=2, relief=tk.SOLID, bg="white", fg="#333333").pack(side=tk.LEFT, expand=True, fill=tk.X)
        # 浏览按钮：缩小尺寸并优化圆角效果
        browse_btn = tk.Button(video_dest_entry_frame, text="浏览", command=self.browse_video_dest,
                             font=('微软雅黑', 8),
                             width=6,
                             height=1,
                             bg="white",
                             fg="#333333",
                             borderwidth=1,
                             relief="ridge",
                             padx=5,
                             pady=3)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # 开始整理按钮：缩小尺寸并优化圆角效果
        process_button = tk.Button(self.root, text="开始整理", command=self.start_processing,
                                 font=('微软雅黑', 8),
                                 width=8,
                                 height=1,
                                 bg="#2561EF",
                                 fg="white",
                                 borderwidth=1,
                                 relief="ridge",
                                 padx=5,
                                 pady=3)
        process_button.pack(pady=15)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="", font=("微软雅黑", 12), bg="#FAFAF2", fg="#666666")
        self.status_label.pack(pady=5)
    
    def browse_source(self):
        directory = filedialog.askdirectory(title="选择原始照片目录", parent=self.root, mustexist=False)
        if directory:
            self.source_dir.set(directory)
    
    def browse_dest(self):
        directory = filedialog.askdirectory(title="选择照片备份目录", parent=self.root, mustexist=False)
        if directory:
            self.dest_dir.set(directory)
    
    def browse_video_dest(self):
        directory = filedialog.askdirectory(title="选择视频备份目录", parent=self.root, mustexist=False)
        if directory:
            self.video_dest_dir.set(directory)
    
    def start_processing(self):
        if self.is_processing:
            return
            
        source = self.source_dir.get()
        photo_dest = self.dest_dir.get()
        video_dest = self.video_dest_dir.get()
        
        if not source:
            messagebox.showerror("错误", "请选择原始照片目录")
            return
        
        # 至少需要选择一个备份目录
        if not photo_dest and not video_dest:
            messagebox.showerror("错误", "请至少选择一个备份目录（照片或视频）")
            return
        
        # 验证目录不能相同
        if photo_dest and source == photo_dest:
            messagebox.showerror("错误", "原始目录和照片备份目录不能相同")
            return
            
        if video_dest and source == video_dest:
            messagebox.showerror("错误", "原始目录和视频备份目录不能相同")
            return
        
        self.is_processing = True
        self.status_label.config(text="正在扫描文件...")
        self.root.update()
        
        try:
            # 获取所有照片和视频文件
            photo_files = []
            video_files = []
            
            if photo_dest:
                photo_files = self.get_all_photo_files(source)
            
            if video_dest:
                video_files = self.get_all_video_files(source)
            
            # 检查是否有文件需要处理
            if not photo_files and not video_files:
                messagebox.showinfo("提示", "未找到需要处理的照片或视频文件")
                self.is_processing = False
                self.status_label.config(text="")
                return
            
            total_files = len(photo_files) + len(video_files)
            self.status_label.config(text="正在整理文件...")
            self.progress_bar.config(maximum=total_files)
            self.progress_var.set(0)
            self.root.update()
            
            # 处理结果统计
            photo_success = 0
            photo_temp = 0
            video_success = 0
            video_temp = 0
            conflict_count = 0
            processed_count = 0
            
            # 处理照片文件
            if photo_files:
                for file_path in photo_files:
                    success = self.process_photo_file(file_path, source, photo_dest)
                    if success == 1:
                        photo_success += 1
                    elif success == 0:
                        photo_temp += 1
                    
                    processed_count += 1
                    self.progress_var.set(processed_count)
                    self.root.update()
            
            # 处理视频文件
            if video_files:
                for file_path in video_files:
                    success = self.process_video_file(file_path, source, video_dest)
                    if success == 1:
                        video_success += 1
                    elif success == 0:
                        video_temp += 1
                    
                    processed_count += 1
                    self.progress_var.set(processed_count)
                    self.root.update()
            
            self.status_label.config(text="整理完成！")
            
            # 构建结果消息
            result_message = "文件整理完成！\n\n"
            
            if photo_files:
                result_message += f"照片处理结果：\n"
                result_message += f"  成功整理: {photo_success} 张\n"
                result_message += f"  放入临时文件夹: {photo_temp} 张\n\n"
            
            if video_files:
                result_message += f"视频处理结果：\n"
                result_message += f"  成功整理: {video_success} 个\n"
                result_message += f"  放入临时文件夹: {video_temp} 个\n"
            
            messagebox.showinfo("成功", result_message)
        except Exception as e:
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
        finally:
            self.is_processing = False
            self.progress_var.set(0)
    
    def get_all_photo_files(self, directory):
        photo_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tif', '.tiff', '.raw']
        photo_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file.lower())[1] in photo_extensions:
                    photo_files.append(os.path.join(root, file))
        
        return photo_files
    
    def get_all_video_files(self, directory):
        video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.webm', '.mpg', '.mpeg']
        video_files = []
        
        for root, _, files in os.walk(directory):
            for file in files:
                if os.path.splitext(file.lower())[1] in video_extensions:
                    video_files.append(os.path.join(root, file))
        
        return video_files
    
    def process_photo_file(self, file_path, source_dir, dest_dir):
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        
        # 解析文件名
        match = re.match(r'.*_([0-9]{8})_.*', file_name)
        if match:
            date_str = match.group(1)
            year = date_str[:4]
            month = date_str[4:6]
            
            # 创建目标目录
            year_dir = os.path.join(dest_dir, year)
            month_dir = os.path.join(year_dir, month)
            
            os.makedirs(month_dir, exist_ok=True)
            
            # 移动文件，处理冲突
            dest_path = os.path.join(month_dir, file_name)
            self.move_file_with_conflict_handling(file_path, dest_path)
            return 1
        else:
            # 非标准格式，放入temp文件夹
            temp_dir = os.path.join(dest_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            dest_path = os.path.join(temp_dir, file_name)
            self.move_file_with_conflict_handling(file_path, dest_path)
            return 0
    
    def process_video_file(self, file_path, source_dir, dest_dir):
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1]
        
        # 解析文件名
        match = re.match(r'.*_([0-9]{8})_.*', file_name)
        if match:
            date_str = match.group(1)
            year = date_str[:4]
            
            # 创建目标目录
            year_dir = os.path.join(dest_dir, year)
            
            os.makedirs(year_dir, exist_ok=True)
            
            # 移动文件，处理冲突
            dest_path = os.path.join(year_dir, file_name)
            self.move_file_with_conflict_handling(file_path, dest_path)
            return 1
        else:
            # 非标准格式，放入temp文件夹
            temp_dir = os.path.join(dest_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            dest_path = os.path.join(temp_dir, file_name)
            self.move_file_with_conflict_handling(file_path, dest_path)
            return 0
    
    def move_file_with_conflict_handling(self, src_path, dest_path):
        if os.path.exists(dest_path):
            src_size = os.path.getsize(src_path)
            dest_size = os.path.getsize(dest_path)
            
            if src_size == dest_size:
                # 文件大小一致，覆盖
                shutil.copy2(src_path, dest_path)
                os.remove(src_path)
            else:
                # 文件大小不一致，重命名
                base_name = os.path.splitext(dest_path)[0]
                ext = os.path.splitext(dest_path)[1]
                counter = 1
                
                while True:
                    new_dest_path = f"{base_name}({counter}){ext}"
                    if not os.path.exists(new_dest_path):
                        shutil.copy2(src_path, new_dest_path)
                        os.remove(src_path)
                        break
                    counter += 1
        else:
            # 目标文件不存在，直接移动
            shutil.copy2(src_path, dest_path)
            os.remove(src_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoOrganizer(root)
    root.mainloop()