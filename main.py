import tkinter as tk
from tkinter import ttk

# 创建主窗口
root = tk.Tk()
root.title("Tkinter 示例程序")
root.geometry("800x600")      # 设置窗口大小
root.resizable(False, False)  # 锁定窗口大小不可调整

# 创建样式对象
style = ttk.Style()
style.theme_use("clam")       # 使用clam主题（支持现代外观）

# ================== 创建页面容器 ==================
# 主页面框架
main_frame = ttk.Frame(root)
main_frame.pack(fill="both", expand=True)  # 填充整个窗口

# 设置页面框架
settings_frame = ttk.Frame(root)

# ================== 主页面元素 ==================
# 标题标签
title_label = ttk.Label(main_frame,
                       text="主页面",
                       font=("微软雅黑", 24))
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# 输入框
entry_label = ttk.Label(main_frame, text="输入姓名:")
entry_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
name_entry = ttk.Entry(main_frame)
name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# 单选按钮
radio_var = tk.StringVar(value="option1")  # 设置默认选项
radio1 = ttk.Radiobutton(main_frame,
                        text="选项1",
                        variable=radio_var,
                        value="option1")
radio2 = ttk.Radiobutton(main_frame,
                        text="选项2",
                        variable=radio_var,
                        value="option2")
radio1.grid(row=2, column=0, columnspan=2, pady=5, sticky="w")
radio2.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

# 复选框
check_var = tk.IntVar()
check_button = ttk.Checkbutton(main_frame,
                             text="同意条款",
                             variable=check_var)
check_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="w")

# 下拉列表
combo_label = ttk.Label(main_frame, text="选择国家:")
combo_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
country_combo = ttk.Combobox(main_frame,
                            values=["中国", "美国", "日本", "德国"])
country_combo.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# 按钮
def show_settings():
    main_frame.pack_forget()        # 隐藏主页面
    settings_frame.pack(fill="both", expand=True)  # 显示设置页面

settings_btn = ttk.Button(main_frame,
                         text="进入设置",
                         command=show_settings)
settings_btn.grid(row=6, column=0, columnspan=2, pady=20)

# ================== 设置页面元素 ==================
# 返回主页面按钮
def show_main():
    settings_frame.pack_forget()    # 隐藏设置页面
    main_frame.pack(fill="both", expand=True)  # 显示主页面

back_btn = ttk.Button(settings_frame,
                     text="返回主页面",
                     command=show_main)
back_btn.pack(pady=20)

# 滑动条
scale_label = ttk.Label(settings_frame, text="音量调节:")
scale_label.pack(pady=5)
volume_scale = ttk.Scale(settings_frame,
                        from_=0,
                        to=100,
                        orient="horizontal")
volume_scale.pack(pady=5, fill="x", padx=50)

# 列表框
listbox_label = ttk.Label(settings_frame, text="选择语言:")
listbox_label.pack(pady=5)
lang_listbox = tk.Listbox(settings_frame)
for lang in ["中文", "English", "Español", "Français"]:
    lang_listbox.insert("end", lang)
lang_listbox.pack(pady=5, fill="both", expand=True, padx=50)

# ================== 启动程序 ==================
root.mainloop()