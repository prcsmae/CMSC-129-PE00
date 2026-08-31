"""
Builds and runs the main application window: input text area, output
text area, Load File button, Process button. Handles all user
interaction (typing, file loading, processing) and window lifecycle.

Calls processor_interface.process_input(lines) and displays
whatever string comes back.
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from processor_interface import process_input


FONT_FAMILY = "Consolas"         
FONT_SIZE = 12

COLOR_FRAME_BG = "#5a5a56"        # outer window / frame background (gray)
COLOR_PANEL_BG = "#6b6b66"        # text area fill (lighter gray)
COLOR_BUTTON_BG = "#4a4a47"       # button fill (darker gray)
COLOR_TEXT = "#ffffff"            # white text



class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Postfix Expression Processor")
        self.geometry("900x560")
        self.minsize(640, 400)
        self.configure(bg=COLOR_FRAME_BG)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._build_left_panel()
        self._build_right_panel()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_left_panel(self):
        left = tk.Frame(self, bg=COLOR_FRAME_BG)
        left.grid(row=0, column=0, sticky="nsew", padx=(16, 8), pady=16)
        left.rowconfigure(0, weight=1)
        left.columnconfigure(0, weight=1)


        input_box = tk.Frame(
            left,
            bg=COLOR_PANEL_BG,
            bd=0,
            highlightthickness=0,
        )
        input_box.grid(row=0, column=0, sticky="nsew")
        input_box.rowconfigure(1, weight=1)
        input_box.columnconfigure(0, weight=1)

        caption = tk.Label(
            input_box,
            text="Input lines:",
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT,
            font=(FONT_FAMILY, FONT_SIZE),
            anchor="w",
        )
        caption.grid(row=0, column=0, sticky="ew", padx=10, pady=(8, 0))

        self.input_text = tk.Text(
            input_box,
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT,
            insertbackground=COLOR_TEXT,
            font=(FONT_FAMILY, FONT_SIZE),
            wrap="none",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=6,
        )
        self.input_text.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 6))
        self.input_text.bind("<KeyRelease>", self._on_input_change)

        # Load File button
        self.load_button = tk.Button(
            left,
            text="Load File",
            command=self.on_load_file,
            bg=COLOR_BUTTON_BG,
            fg=COLOR_TEXT,
            activebackground=COLOR_BUTTON_BG,
            activeforeground=COLOR_TEXT,
            font=(FONT_FAMILY, FONT_SIZE),
            relief="flat",
            bd=0,
            padx=8,
            pady=8,
        )
        self.load_button.grid(row=1, column=0, sticky="ew", pady=(10, 0))

    def _build_right_panel(self):
        right = tk.Frame(self, bg=COLOR_FRAME_BG)
        right.grid(row=0, column=1, sticky="nsew", padx=(8, 16), pady=16)
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)

        output_box = tk.Frame(
            right,
            bg=COLOR_PANEL_BG,
            bd=0,
            highlightthickness=0,
        )
        output_box.grid(row=0, column=0, sticky="nsew")
        output_box.rowconfigure(0, weight=1)
        output_box.columnconfigure(0, weight=1)

        self.output_text = tk.Text(
            output_box,
            bg=COLOR_PANEL_BG,
            fg=COLOR_TEXT,
            font=(FONT_FAMILY, FONT_SIZE),
            wrap="word",
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=8,
            state="disabled",  # read-only
        )
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        # Process button
        self.process_button = tk.Button(
            right,
            text="Process",
            command=self.on_process,
            bg=COLOR_BUTTON_BG,
            fg=COLOR_TEXT,
            activebackground=COLOR_BUTTON_BG,
            activeforeground=COLOR_TEXT,
            font=(FONT_FAMILY, FONT_SIZE),
            relief="flat",
            bd=0,
            padx=8,
            pady=8,
            state="disabled",  
        )
        self.process_button.grid(row=1, column=0, sticky="ew", pady=(10, 0))

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------
    def _on_input_change(self, event=None):
        has_content = bool(self.input_text.get("1.0", tk.END).strip())
        self.process_button.config(state="normal" if has_content else "disabled")

    def on_load_file(self):
        filepath = filedialog.askopenfilename(
            title="Load input file",
            filetypes=[("Input files", "*.in")],
        )
        if not filepath:
            return

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError) as e:
            messagebox.showerror("Error loading file", f"Could not read file:\n{e}")
            return

        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", content)
        self._on_input_change()

    def on_process(self):
        content = self.input_text.get("1.0", tk.END)
        if not content.strip():
            messagebox.showwarning("Empty input", "The input text area is empty.")
            return

        lines = content.splitlines()
        result = process_input(lines)

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)
        self.output_text.config(state="disabled")


def run():
    app = App()
    app.mainloop()
