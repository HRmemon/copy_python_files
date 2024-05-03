import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import pyperclip
from copy_files import copy_files_to_clipboard

class FileProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Processor GUI")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("size", "type"), show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.populate_tree(Path().resolve())  # Start at the user's home directory

        self.options_frame = ttk.LabelFrame(self, text="Options")
        self.options_frame.pack(fill=tk.X, expand=False)

        self.modify_python_var = tk.BooleanVar(value=True)
        self.chk_modify_python = ttk.Checkbutton(self.options_frame, text="Modify Python Files", variable=self.modify_python_var)
        self.chk_modify_python.pack(side=tk.LEFT)

        self.btn_process = ttk.Button(self.options_frame, text="Process Selected", command=self.process_selected)
        self.btn_process.pack(side=tk.RIGHT)

    def populate_tree(self, start_path):
        node = self.tree.insert('', 'end', text=start_path.name, open=True, values=("", "directory"))
        self.process_directory(node, start_path)

    def process_directory(self, parent, path):
        for p in path.iterdir():
            oid = self.tree.insert(parent, 'end', text=p.name, open=False, values=(p.stat().st_size, "file" if p.is_file() else "directory"))
            if p.is_dir():
                self.process_directory(oid, p)

    def process_selected(self):
        selected_items = self.tree.selection()
        files = []
        for item in selected_items:
            path = self.get_full_path(item)
            files.append(path)
        
        # remove directories from the list
        files = [f for f in files if os.path.isfile(f)]
        copy_files_to_clipboard(files)

        # close the window
        self.destroy()
        
        #     print(f"Processing: {path}")
            # Here, you would call your existing process logic
            # self.copy_to_clipboard(path, self.modify_python_var.get(), ...)

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
