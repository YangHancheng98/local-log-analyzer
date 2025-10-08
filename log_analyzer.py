import tkinter as tk
from tkinter import filedialog, messagebox
import yaml
import os
import re
from glob import glob

# 读取 YAML 规则
def load_rules(rule_file):
    if not os.path.exists(rule_file):
        return []
    with open(rule_file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []

# 扫描日志文件夹
def collect_log_files(path):
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        files = glob(os.path.join(path, "**", "*.txt"), recursive=True)
        files += glob(os.path.join(path, "**", "*.log"), recursive=True)
        return files
    return []

# 分析日志文件
def analyze_log(log_files, rules):
    matched_lines = []
    for file in log_files:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception as e:
            matched_lines.append((f"[无法读取文件 {file}: {e}]", "gray"))
            continue

        for i, line in enumerate(lines, start=1):
            line = line.strip()
            for rule in rules:
                keyword = rule.get("keyword")
                color = rule.get("color", "black")
                is_regex = rule.get("regex", False)
                instruction = rule.get("instruction", "")

                if not keyword:
                    continue

                # # 调试输出
                # print(f"匹配规则: {keyword}, is_regex={is_regex}, 行内容: {line[:50]}")

                try:
                    if is_regex:
                        matched = re.search(keyword, line, re.IGNORECASE)
                    else:
                        matched = keyword.lower() in line.lower()
                except re.error as e:
                    # print(f"正则错误: {keyword} -> {e}")
                    matched = False

                if matched:
                    info = f"[{os.path.basename(file)}:{i}] {line}"
                    if instruction:
                        info += f"  ← {instruction}"
                    matched_lines.append((info, color))
                    # 匹配到后跳出当前规则循环
                    break
    return matched_lines

# GUI 逻辑
def browse_log():
    path = filedialog.askopenfilename(filetypes=[("Log/Txt Files", "*.log *.txt")])
    if not path:
        path = filedialog.askdirectory()
    if path:
        log_path_var.set(path)

def browse_rule():
    rule_path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yaml *.yml")])
    if rule_path:
        rule_path_var.set(rule_path)

def clear_rule():
    rule_path_var.set("")

current_logs = []  # 全局变量，保存当前显示的日志

def clear_log_display():
    global current_logs
    current_logs = []  # 清空内存里的日志
    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)
    text_box.config(state=tk.DISABLED)


def analyze():
    global current_logs
    current_logs = []
    log_path = log_path_var.get()
    rule_file = rule_path_var.get()

    if not log_path:
        messagebox.showwarning("警告", "请选择日志文件或文件夹！")
        return

    rules = load_rules(rule_file) if rule_file else []
    # print("读取的规则：", rules)
    log_files = collect_log_files(log_path)
    # print("收集到的日志文件：", log_files)
    if not log_files:
        messagebox.showwarning("提示", "未找到任何日志文件 (.log / .txt)")
        return

    matched_lines = analyze_log(log_files, rules)

    text_box.config(state=tk.NORMAL)
    text_box.delete("1.0", tk.END)

    if matched_lines:
        for line, color in matched_lines:
            text_box.insert(tk.END, line + "\n", color)
            current_logs.append(line)  # 保存到列表
    else:
        text_box.insert(tk.END, "未匹配到任何规则。\n", "gray")
        current_logs.append("未匹配到任何规则。")

    text_box.config(state=tk.DISABLED)

def export_logs():
    if not current_logs:
        messagebox.showinfo("提示", "当前没有日志可导出")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("\n".join(current_logs))
            messagebox.showinfo("成功", f"日志已保存到 {file_path}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {e}")

# 主窗口
root = tk.Tk()
root.title("日志分析工具 (Tkinter版 - instruction支持)")
root.geometry("900x650")
root.resizable(True, True)

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="日志文件/文件夹:").grid(row=0, column=0, padx=5)
log_path_var = tk.StringVar()
tk.Entry(frame_top, textvariable=log_path_var, width=60).grid(row=0, column=1, padx=5)
tk.Button(frame_top, text="浏览", command=browse_log).grid(row=0, column=2, padx=5)

tk.Label(frame_top, text="规则文件:").grid(row=1, column=0, padx=5)
rule_path_var = tk.StringVar()
tk.Entry(frame_top, textvariable=rule_path_var, width=60).grid(row=1, column=1, padx=5)
tk.Button(frame_top, text="浏览", command=browse_rule).grid(row=1, column=2, padx=5)
tk.Button(frame_top, text="清空规则", command=clear_rule).grid(row=1, column=3, padx=5)

tk.Button(frame_top, text="开始分析", command=analyze, bg="#4CAF50", fg="white").grid(row=2, column=1, pady=10)
tk.Button(frame_top, text="导出日志", command=export_logs, bg="#2196F3", fg="white").grid(row=2, column=3, pady=10)
tk.Button(frame_top, text="清空日志", command=clear_log_display, bg="#F44336", fg="white").grid(row=2, column=2, pady=10)

text_box = tk.Text(
    root,
    wrap=tk.WORD,
    bg="black",       # 背景黑色
    fg="white",       # 默认字体白色
    insertbackground="white"  # 光标也用白色
)
text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
scrollbar = tk.Scrollbar(text_box)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)

# 定义颜色样式
custom_colors = {
    "red": "#FF5555",
    "orange": "#FFAA00",
    "yellow": "#FFFF55",
    "green": "#55FF55",
    "cyan": "#55FFFF",
    "blue": "#55AAFF",
    "purple": "#AA55FF",
    "pink": "#FF55AA",
    "gray": "#AAAAAA",
    "black": "white"  # 避免黑底黑字
}
for name, hexcolor in custom_colors.items():
    text_box.tag_config(name, foreground=hexcolor)

root.mainloop()
