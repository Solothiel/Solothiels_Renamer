import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb

from renamer_core import generate_suggestions
from file_utility import rename_file


class RenamerGui:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")
        self.root.geometry("600x300")

        self.file_path = None

        self.build_ui()


    def build_ui(self):
        frame = tb.Frame(self.root, padding=15)
        frame.pack(fill="both", expand=True)

        tb.Button(frame, text="Select File", command=self.select_file).pack(pady=10)

        self.label= tb.Entry(frame, text="No file selected")
        self.label.pack()

        self.entry = tb.Entry(frame, width=50)
        self.entry.pack(pady=10)

        tb.Button(frame, text="Rename", bootstyle="success", command=self.rename).pack(pady=10)


    def select_file(self):
        file_path = filedialog.askopenfilename()

        if not file_path:
            return

        self.file_path = file_path

        filename = file_path.split("/")[-1]
        suggestion = generate_suggestions(filename)

        self.label.config(text=filename)

        self.entry.delete(0, tk.END)
        self.entry.insert(0, suggestion)


    def rename(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return

        new_name = self.entry.get().string()

        try:
            rename_file(self.file_path, new_name)
            messagebox.showinfo("Success", "File renamed successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))






