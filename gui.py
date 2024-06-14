import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import pyperclip
from copy_files import copy_files_to_clipboard
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os

class Filter:
    def __init__(self):
        self.include = set()
        self.exclude = set()

    def update(self, include_str="", exclude_str="", dot_prefix=False):
        if include_str:
            self.include.update(self._parse(include_str, dot_prefix))
        if exclude_str:
            self.exclude.update(self._parse(exclude_str, dot_prefix))

    def match(self, name, extension=None):
        if self.include and (name not in self.include and (extension not in self.include if extension else True)):
            return False
        if self.exclude and (name in self.exclude or (extension in self.exclude if extension else False)):
            return False
        return True

    @staticmethod
    def _parse(filter_str, dot_prefix=False):
        return {f.strip() if not dot_prefix else f'.{f.strip()}' for f in filter_str.split(',')}

class FileProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Processor GUI")
        self.geometry("800x600")

        self.file_filter = Filter()
        self.directory_filter = Filter()
        self.extension_filter = Filter()

        self.create_widgets()

    def create_widgets(self):
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("size", "type"), show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, expand=False)

        self.setup_filter_widgets("Include", self.update_filters)
        self.setup_filter_widgets("Exclude", self.update_filters)

        self.btn_process = ttk.Button(self.options_frame, text="Process Selected", command=self.process_selected)
        self.btn_process.grid(row=4, column=1, columnspan=2)

        self.populate_tree(Path().resolve())

    def setup_filter_widgets(self, label_text, command):
        base_row = 0 if "Include" in label_text else 3
        lbl_frame = ttk.Label(self.options_frame, text=f"{label_text} Filters:")
        lbl_frame.grid(row=base_row, column=0, columnspan=2)

        for i, (text, var_name) in enumerate([("Files", "file_var"), ("Directories", "dir_var"), ("Extensions", "ext_var")]):
            setattr(self, f"{label_text.lower()}_{var_name}", tk.StringVar())
            lbl = ttk.Label(self.options_frame, text=text)
            lbl.grid(row=base_row + i + 1, column=0)
            entry = ttk.Entry(self.options_frame, width=20, textvariable=getattr(self, f"{label_text.lower()}_{var_name}"))
            entry.grid(row=base_row + i + 1, column=1)
            getattr(self, f"{label_text.lower()}_{var_name}").trace_add("write", command)

    def update_filters(self, *args):
        self.file_filter.update(self.include_file_var.get(), self.exclude_file_var.get())
        self.directory_filter.update(self.include_dir_var.get(), self.exclude_dir_var.get())
        self.extension_filter.update(self.include_ext_var.get(), self.exclude_ext_var.get(), dot_prefix=True)
        self.populate_tree(Path().resolve())

    def populate_tree(self, start_path):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.process_directory('', start_path)

    def process_directory(self, parent, path):
        for p in path.iterdir():
            if p.is_dir() and self.directory_filter.match(p.name):
                oid = self.tree.insert(parent, 'end', text=p.name, open=False, values=(p.stat().st_size, "directory"))
                self.process_directory(oid, p)
            elif p.is_file() and self.file_filter.match(p.name, p.suffix):
                self.tree.insert(parent, 'end', text=p.name, open=False, values=(p.stat().st_size, "file"))

    def process_selected(self):
        selected_items = self.tree.selection()
        files = [self.get_full_path(item) for item in selected_items if os.path.isfile(self.get_full_path(item))]
        # Example of processing: printing paths
        for file in files:
            print(f"Processing: {file}")

    def get_full_path(self, item):
        path = self.tree.item(item, 'text')
        parent = self.tree.parent(item)
        while parent:
            path = os.path.join(self.tree.item(parent, 'text'), path)
            parent = self.tree.parent(parent)
        return '/'.join(path.split(os.sep)[1:])

if __name__ == "__main__":
    app = FileProcessorApp()
    app.mainloop()
