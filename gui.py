import os
import tkinter as tk
import ttkbootstrap as tb
from tkinter import filedialog, messagebox

from renamer_core import generate_suggestions
from file_utility import rename_file
from history_manager import pop_last
from tkinterdnd2 import DND_FILES


class RenamerGui:
    def __init__(self, root):
        self.root = root
        self.root.title("☾ Solothiel's Renamer ☽")
        self.root.geometry("850x600")

        self.files = []
        self.preview_data = []

        self.build_ui()
        self.enable_drag_drop()

    # ---------------- UI ----------------
    def build_ui(self):

        header = tb.Label(
            self.root,
            text="☾ Solothiel's BATCH RENAMER ☽",
            font=("Segoe UI", 18, "bold")
        )
        header.pack(pady=10)

        btn_frame = tb.Frame(self.root)
        btn_frame.pack(fill="x", padx=10)

        tb.Button(btn_frame, text="Add Files", bootstyle="primary", command=self.add_files).pack(side="left")
        tb.Button(btn_frame, text="Undo Last", bootstyle="warning", command=self.undo).pack(side="left", padx=5)
        tb.Button(btn_frame, text="Rename All", bootstyle="success", command=self.rename_all).pack(side="right")

        # Preview table
        self.tree = tb.Treeview(self.root, columns=("old", "new"), show="headings", height=18)
        self.tree.heading("old", text="Original File")
        self.tree.heading("new", text="Suggested Name")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.log = tb.Text(self.root, height=8)
        self.log.pack(fill="x", padx=10, pady=5)

    # ---------------- Drag & Drop ----------------
    def enable_drag_drop(self):
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind("<<Drop>>", self.handle_drop)

    def handle_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        self.files.extend(files)
        self.refresh_preview()

    # ---------------- File Input ----------------
    def add_files(self):
        files = filedialog.askopenfilenames()
        self.files.extend(files)
        self.refresh_preview()

    # ---------------- Preview ----------------
    def refresh_preview(self):
        self.tree.delete(*self.tree.get_children())
        self.preview_data = []

        for f in self.files:
            base = os.path.basename(f)
            suggestion = generate_suggestions(base)

            self.preview_data.append((f, suggestion))
            self.tree.insert("", "end", values=(base, suggestion))

    # ---------------- Rename ----------------
    def rename_all(self):
        for old_path, new_name in self.preview_data:
            try:
                new_path = rename_file(old_path, new_name)
                self.log.insert("end", f"Renamed: {old_path} → {new_path}\n")
            except Exception as e:
                self.log.insert("end", f"Error: {e}\n")

        self.files.clear()
        self.refresh_preview()

    # ---------------- Undo ----------------
    def undo(self):
        last = pop_last()
        if not last:
            messagebox.showinfo("Undo", "Nothing to undo")
            return

        try:
            from file_utility import undo_rename
            undo_rename(last["old"], last["new"])
            self.log.insert("end", f"Undo: {last['new']} → {last['old']}\n")
        except Exception as e:
            messagebox.showerror("Undo Error", str(e))