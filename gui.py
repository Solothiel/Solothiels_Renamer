import os
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb

from renamer_core import generate_suggestions
from file_utility import rename_file


class RenamerGui:
    def __init__(self, root):
        self.root = root

        self.root.title("☾ Solothiel's File Renamer ☽")
        self.root.geometry("750x450")
        self.root.minsize(700, 400)

        self.file_path = None

        self.build_ui()

    def build_ui(self):

        # =========================
        # HEADER
        # =========================
        header_frame = tb.Frame(self.root, padding=10)
        header_frame.pack(fill=tk.X)

        header_title = tb.Label(
            header_frame,
            text="☾ Solothiel's File Renamer ☽",
            font=("Segoe UI", 16, "bold"),
            foreground="#FFFFFF",
            background="#0A0A0A"
        )
        header_title.pack(side=tk.LEFT)

        # =========================
        # BODY
        # =========================
        body_frame = tb.Frame(self.root, padding=20)
        body_frame.pack(fill=tk.BOTH, expand=True)

        # =========================
        # CONFIGURATION PANEL
        # =========================
        config_frame = tb.Labelframe(
            body_frame,
            text=" FILE RENAMING PANEL ",
            bootstyle="secondary"
        )
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # File Select Button
        self.select_button = tb.Button(
            config_frame,
            text="☾ SELECT FILE ☽",
            bootstyle="light",
            command=self.select_file,
            width=18
        )
        self.select_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        # Selected File Label
        self.label = tb.Label(
            config_frame,
            text="No file selected",
            font=("Helvetica", 9, "italic")
        )
        self.label.grid(
            row=0,
            column=1,
            sticky="w",
            padx=10
        )

        # Suggested Name Label
        tb.Label(
            config_frame,
            text="Suggested Name:",
            font=("Helvetica", 10, "bold")
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=10,
            pady=10
        )

        # Rename Entry
        self.entry = tb.Entry(
            config_frame,
            width=50
        )
        self.entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # Rename Button
        self.rename_button = tb.Button(
            config_frame,
            text="☾ EXECUTE RENAME ☽",
            bootstyle="success",
            command=self.rename
        )
        self.rename_button.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=15
        )

        config_frame.columnconfigure(1, weight=1)

        # =========================
        # STATUS SECTION
        # =========================
        self.status_label = tb.Label(
            body_frame,
            text="Renamer idle. Awaiting file selection.",
            font=("Helvetica", 9, "italic")
        )
        self.status_label.pack(
            anchor=tk.W,
            pady=(0, 10)
        )

        # =========================
        # ACTIVITY LOG
        # =========================
        log_frame = tb.Frame(body_frame)
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.log_area = tb.Text(
            log_frame,
            wrap=tk.WORD,
            height=10,
            font=("Consolas", 10)
        )
        self.log_area.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar = tb.Scrollbar(
            log_frame,
            orient="vertical",
            bootstyle="secondary",
            command=self.log_area.yview
        )
        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.log_area.configure(
            yscrollcommand=scrollbar.set
        )

        self.log("[SYSTEM] Solothiel's Renamer initialized.")

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)

    def select_file(self):
        file_path = filedialog.askopenfilename()

        if not file_path:
            return

        self.file_path = file_path

        filename = os.path.basename(file_path)

        self.label.config(text=filename)

        self.status_label.config(
            text=f"Target acquired: {filename}"
        )

        self.log(f"[TARGET] {filename}")

        try:
            suggestion = generate_suggestions(filename)

            self.entry.delete(0, tk.END)
            self.entry.insert(0, suggestion)

            self.log(
                f"[AI] Suggested filename generated: {suggestion}"
            )

        except Exception as e:
            self.log(f"[ERROR] {e}")
            messagebox.showerror(
                "Suggestion Error",
                str(e)
            )

    def rename(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected")
            return

        new_name = self.entry.get().strip()

        if not new_name:
            messagebox.showerror("Error", "Please enter a filename.")
            return

        # prevent users from breaking extension logic
        new_name = os.path.splitext(new_name)[0]

        try:
            old_name = os.path.basename(self.file_path)

            rename_file(self.file_path, new_name)

            self.status_label.config(
                text=f"{old_name} → {new_name}"
            )

            self.log(f"[SUCCESS] {old_name} → {new_name}")

            messagebox.showinfo("Success", "File renamed successfully.")

        except Exception as e:
            self.log(f"[ERROR] {e}")
            messagebox.showerror("Rename Error", str(e))


