import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import pyperclip
from copy_files import process_content

class FileProcessorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File Processor")
        self.geometry("800x600")

        self.selected_files = []
        self.directory = None
        self.init_ui()

    def init_ui(self):
        self.create_menu()
        self.create_treeview()
        self.create_filters()
        self.create_options()
        self.create_run_button()

    def create_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Directory", command=self.open_directory)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

    def create_treeview(self):
        self.tree = ttk.Treeview(self, columns=("path",), selectmode="extended")
        self.tree.heading("#0", text="Files and Folders")
        self.tree.heading("path", text="Path")
        self.tree.column("path", width=0, stretch=tk.NO)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def create_filters(self):
        filter_frame = tk.Frame(self)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Include Extensions:").grid(row=0, column=0, padx=5, pady=5)
        self.include_ext_entry = tk.Entry(filter_frame)
        self.include_ext_entry.grid(row=0, column=1, padx=5, pady=5)
        self.include_ext_entry.bind("<KeyRelease>", lambda event: self.update_treeview())

        tk.Label(filter_frame, text="Exclude Extensions:").grid(row=0, column=2, padx=5, pady=5)
        self.exclude_ext_entry = tk.Entry(filter_frame)
        self.exclude_ext_entry.grid(row=0, column=3, padx=5, pady=5)
        self.exclude_ext_entry.bind("<KeyRelease>", lambda event: self.update_treeview())

        tk.Label(filter_frame, text="Include Directories:").grid(row=1, column=0, padx=5, pady=5)
        self.include_dirs_entry = tk.Entry(filter_frame)
        self.include_dirs_entry.grid(row=1, column=1, padx=5, pady=5)
        self.include_dirs_entry.bind("<KeyRelease>", lambda event: self.update_treeview())

        tk.Label(filter_frame, text="Exclude Directories:").grid(row=1, column=2, padx=5, pady=5)
        self.exclude_dirs_entry = tk.Entry(filter_frame)
        self.exclude_dirs_entry.grid(row=1, column=3, padx=5, pady=5)
        self.exclude_dirs_entry.bind("<KeyRelease>", lambda event: self.update_treeview())

    def create_options(self):
        option_frame = tk.Frame(self)
        option_frame.pack(fill=tk.X, padx=10, pady=5)

        self.modify_python_var = tk.BooleanVar(value=True)
        tk.Checkbutton(option_frame, text="Modify Python Files", variable=self.modify_python_var).pack(anchor=tk.W)

    def create_run_button(self):
        run_button = tk.Button(self, text="Run", command=self.run_processing)
        run_button.pack(pady=10)

    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.directory = directory
            self.update_treeview()

    def update_treeview(self):
        include_ext = self.include_ext_entry.get().split() if self.include_ext_entry.get() else None
        exclude_ext = self.exclude_ext_entry.get().split() if self.exclude_ext_entry.get() else None
        include_dirs = self.include_dirs_entry.get().split() if self.include_dirs_entry.get() else None
        exclude_dirs = self.exclude_dirs_entry.get().split() if self.exclude_dirs_entry.get() else None

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.populate_tree(self.directory, include_ext, exclude_ext, include_dirs, exclude_dirs)

    def populate_tree(self, directory, include_ext, exclude_ext, include_dirs, exclude_dirs):
        def should_include_dir(d):
            if include_dirs and d not in include_dirs:
                return False
            if exclude_dirs and d in exclude_dirs:
                return False
            return True

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if should_include_dir(d)]
            filtered_files = [f for f in files if self.should_include_file(f, include_ext, exclude_ext)]

            if filtered_files or dirs:
                path = root.replace(directory, "").lstrip(os.sep)
                parent = ""
                if path:
                    parent = self.tree.insert("", "end", text=path, open=True)
                self.insert_items(parent, root, filtered_files, include_ext, exclude_ext)
    
    def should_include_file(self, file, include_ext, exclude_ext):
        suffix = Path(file).suffix
        if include_ext and suffix not in include_ext:
            return False
        if exclude_ext and suffix in exclude_ext:
            return False
        return True

    def insert_items(self, parent, path, files, include_ext, exclude_ext):
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                filtered_files = [f for f in os.listdir(full_path) if self.should_include_file(f, include_ext, exclude_ext)]
                if filtered_files or [d for d in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, d))]:
                    node = self.tree.insert(parent, "end", text=item, values=(full_path,))
                    self.insert_items(node, full_path, filtered_files, include_ext, exclude_ext)
            else:
                if item in files:
                    self.tree.insert(parent, "end", text=item, values=(full_path,))

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        self.selected_files = [self.tree.item(item, "values")[0] for item in selected_items if self.tree.item(item, "values")]

    def run_processing(self):
        if not self.selected_files:
            messagebox.showwarning("No Selection", "Please select at least one file or directory.")
            return

        include_ext = self.include_ext_entry.get().split() if self.include_ext_entry.get() else None
        exclude_ext = self.exclude_ext_entry.get().split() if self.exclude_ext_entry.get() else None
        include_dirs = self.include_dirs_entry.get().split() if self.include_dirs_entry.get() else None
        exclude_dirs = self.exclude_dirs_entry.get().split() if self.exclude_dirs_entry.get() else None
        modify_python = self.modify_python_var.get()

        clipboard_content = ""
        for path in self.selected_files:
            if os.path.isfile(path):
                clipboard_content += self.process_file(path, modify_python)
            elif os.path.isdir(path):
                clipboard_content += self.process_directory(path, include_ext, exclude_ext, include_dirs, exclude_dirs, modify_python)

        pyperclip.copy(clipboard_content.strip())
        messagebox.showinfo("Processing Complete", "Selected files have been processed and copied to clipboard.")

    def process_file(self, file_path, modify_python):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        modified_content = process_content(content, modify_python and Path(file_path).suffix == '.py')
        return f"# File: {file_path}\n{modified_content}\n\n"

    def process_directory(self, directory, include_ext, exclude_ext, include_dirs, exclude_dirs, modify_python):
        clipboard_content = ""
        for root, dirs, files in os.walk(directory):
            if include_dirs:
                dirs[:] = [d for d in dirs if d in include_dirs]
            if exclude_dirs:
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                file_path = Path(root) / file
                if include_ext and not file_path.suffix in include_ext:
                    continue
                if exclude_ext and file_path.suffix in exclude_ext:
                    continue

                clipboard_content += self.process_file(file_path, modify_python)

        return clipboard_content

if __name__ == "__main__":
    app = FileProcessorApp()
    app.mainloop()
