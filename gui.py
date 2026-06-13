import os
import tkinter as tk
import ttkbootstrap as tb
from tkinter import filedialog, messagebox

from renamer_core import generate_suggestions
from file_utility import rename_file


class RenamerGui:
    def __init__(self, root):
        self.root = root
        self.root.title("☾ Moon Knight Excel Renamer ☽")
        self.root.geometry("900x600")

        self.files = []
        self.row_map = {}  # tree item → file path

        self.build_ui()

    # ================= UI =================
    def build_ui(self):

        header = tb.Label(
            self.root,
            text="☾ EXCEL-STYLE BATCH RENAMER ☽",
            font=("Segoe UI", 18, "bold")
        )
        header.pack(pady=10)

        # Buttons
        btn_frame = tb.Frame(self.root)
        btn_frame.pack(fill="x", padx=10)

        tb.Button(btn_frame, text="Add Files", bootstyle="primary", command=self.add_files).pack(side="left")
        tb.Button(btn_frame, text="Rename All", bootstyle="success", command=self.rename_all).pack(side="right")

        # ================= TABLE =================
        self.tree = tb.Treeview(
            self.root,
            columns=("original", "new"),
            show="headings",
            height=20
        )

        self.tree.heading("original", text="Original File")
        self.tree.heading("new", text="New Name (Double Click to Edit)")

        self.tree.column("original", width=400)
        self.tree.column("new", width=400)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # bind excel-style edit
        self.tree.bind("<Double-1>", self.edit_cell)

        # log
        self.log = tb.Text(self.root, height=6)
        self.log.pack(fill="x", padx=10)

    # ================= FILE INPUT =================
    def add_files(self):
        files = filedialog.askopenfilenames()
        if not files:
            return

        for f in files:
            base = os.path.basename(f)
            suggestion = generate_suggestions(base)

            item = self.tree.insert("", "end", values=(base, suggestion))
            self.row_map[item] = f

        self.log.insert("end", f"Added {len(files)} files\n")

    # ================= EXCEL EDITING =================
    def edit_cell(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        # Only allow editing "new name" column (#2)
        if column != "#2":
            return

        x, y, width, height = self.tree.bbox(row_id, column)
        old_value = self.tree.set(row_id, "new")

        entry = tb.Entry(self.root)
        entry.place(x=x + 10, y=y + 80, width=width)
        entry.insert(0, old_value)
        entry.focus()

        def save(event=None):
            self.tree.set(row_id, "new", entry.get())
            entry.destroy()

        entry.bind("<Return>", save)
        entry.bind("<FocusOut>", save)

    # ================= RENAME =================
    def rename_all(self):
        for row in self.tree.get_children():
            old_name, new_name = self.tree.item(row)["values"]
            file_path = self.row_map[row]

            try:
                rename_file(file_path, new_name)
                self.log.insert("end", f"Renamed: {old_name} → {new_name}\n")

            except Exception as e:
                self.log.insert("end", f"Error: {e}\n")

        self.tree.delete(*self.tree.get_children())
        self.row_map.clear()

        self.log.insert("end", "Batch complete\n")