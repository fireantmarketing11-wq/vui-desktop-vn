"""Giao diện chính bằng Tkinter (tiếng Việt)"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from . import emoji_art, jokes

BASE = Path(__file__).resolve().parents[1]
DATA_DIR = BASE / "data"


def run_app():
    root = tk.Tk()
    root.title("Vui Desktop VN — Emoji + Truyện cười")
    root.geometry("700x450")

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except Exception:
        pass

    nb = ttk.Notebook(root)
    nb.pack(fill=tk.BOTH, expand=True)

    # Emoji tab
    frm_emoji = ttk.Frame(nb)
    nb.add(frm_emoji, text="Emoji art")

    left_e = ttk.Frame(frm_emoji)
    left_e.pack(side=tk.LEFT, fill=tk.Y, padx=8, pady=8)

    lbl_templates = ttk.Label(left_e, text="Mẫu:")
    lbl_templates.pack(anchor=tk.W)

    templates = emoji_art.get_template_names()
    lb_templates = tk.Listbox(left_e, height=12)
    for t in templates:
        lb_templates.insert(tk.END, t)
    lb_templates.pack(fill=tk.Y, expand=False)

    btn_preview = ttk.Button(left_e, text="Xem mẫu",
                             command=lambda: show_emoji())
    btn_preview.pack(fill=tk.X, pady=4)

    btn_copy = ttk.Button(left_e, text="Sao chép vào clipboard",
                          command=lambda: copy_to_clipboard())
    btn_copy.pack(fill=tk.X, pady=4)

    btn_save = ttk.Button(left_e, text="Lưu ra file .txt",
                          command=lambda: save_emoji())
    btn_save.pack(fill=tk.X, pady=4)

    right_e = ttk.Frame(frm_emoji)
    right_e.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

    lbl_preview = ttk.Label(right_e, text="Xem trước:")
    lbl_preview.pack(anchor=tk.W)

    txt_preview = tk.Text(right_e, wrap=tk.NONE, font=("Consolas", 14))
    txt_preview.pack(fill=tk.BOTH, expand=True)
    txt_preview.configure(state=tk.DISABLED)

    # Jokes tab
    frm_jokes = ttk.Frame(nb)
    nb.add(frm_jokes, text="Truyện cười")

    top_j = ttk.Frame(frm_jokes)
    top_j.pack(fill=tk.X, padx=8, pady=8)

    btn_next = ttk.Button(top_j, text="Truyện mới", command=lambda: show_joke())
    btn_next.pack(side=tk.LEFT)

    btn_copy_j = ttk.Button(top_j, text="Sao chép truyện", command=lambda: copy_joke())
    btn_copy_j.pack(side=tk.LEFT, padx=6)

    btn_save_j = ttk.Button(top_j, text="Lưu truyện", command=lambda: save_joke())
    btn_save_j.pack(side=tk.LEFT)

    txt_joke = tk.Text(frm_jokes, wrap=tk.WORD, font=("Arial", 12))
    txt_joke.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0,8))
    txt_joke.configure(state=tk.DISABLED)

    # status bar
    status = tk.StringVar(value="Sẵn sàng")
    statusbar = ttk.Label(root, textvariable=status, relief=tk.SUNKEN, anchor=tk.W)
    statusbar.pack(fill=tk.X, side=tk.BOTTOM)

    # helper closures
    def set_status(s):
        status.set(s)

    def show_emoji():
        sel = lb_templates.curselection()
        if not sel:
            messagebox.showinfo("Chọn mẫu", "Vui lòng chọn một mẫu bên trái.")
            return
        name = lb_templates.get(sel[0])
        art = emoji_art.generate(name)
        txt_preview.configure(state=tk.NORMAL)
        txt_preview.delete("1.0", tk.END)
        txt_preview.insert(tk.END, art)
        txt_preview.configure(state=tk.DISABLED)
        set_status(f"Đang hiển thị: {name}")

    def copy_to_clipboard():
        sel = lb_templates.curselection()
        if not sel:
            messagebox.showinfo("Chọn mẫu", "Vui lòng chọn một mẫu để sao chép.")
            return
        name = lb_templates.get(sel[0])
        art = emoji_art.generate(name)
        root.clipboard_clear()
        root.clipboard_append(art)
        set_status("Đã sao chép vào clipboard.")

    def save_emoji():
        sel = lb_templates.curselection()
        if not sel:
            messagebox.showinfo("Chọn mẫu", "Vui lòng chọn một mẫu để lưu.")
            return
        name = lb_templates.get(sel[0])
        art = emoji_art.generate(name)
        f = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Text files","*.txt")],
                                         title="Lưu emoji art")
        if f:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(art)
            set_status(f"Đã lưu: {f}")

    current_joke = {"text": ""}

    def show_joke():
        j = jokes.get_random_joke()
        current_joke["text"] = j
        txt_joke.configure(state=tk.NORMAL)
        txt_joke.delete("1.0", tk.END)
        txt_joke.insert(tk.END, j)
        txt_joke.configure(state=tk.DISABLED)
        set_status("Hiển thị truyện mới")

    def copy_joke():
        if not current_joke["text"]:
            messagebox.showinfo("Chưa có truyện", "Nhấn 'Truyện mới' để lấy truyện trước khi sao chép.")
            return
        root.clipboard_clear()
        root.clipboard_append(current_joke["text"])
        set_status("Đã sao chép truyện vào clipboard")

    def save_joke():
        if not current_joke["text"]:
            messagebox.showinfo("Chưa có truyện", "Nhấn 'Truyện mới' để lấy truyện trước khi lưu.")
            return
        f = filedialog.asksaveasfilename(defaultextension=".txt",
                                         filetypes=[("Text files","*.txt")],
                                         title="Lưu truyện cười")
        if f:
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(current_joke["text"])
            set_status(f"Đã lưu: {f}")

    # show initial joke
    show_joke()

    root.mainloop()
