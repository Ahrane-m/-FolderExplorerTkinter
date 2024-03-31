import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json


class FolderExplorerApp:
    def __init__(self, root):
        """
        Initialize the FolderExplorerApp.

        Parameters:
            root (tk.Tk): The root window of the application.
        """
        self.root = root
        self.root.title("Folder Explorer")

        # Create tree view
        self.tree = ttk.Treeview(root, selectmode="extended", height=15)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize selected files list
        self.selected_files = []

        # Bind button release event to handle file selection
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        # Attach button
        self.attach_button = tk.Button(root, text="Attach", command=self.attach_files, width=15)
        self.attach_button.pack(side=tk.LEFT, padx=(10, 5), pady=5)

        # Detach button
        self.detach_button = tk.Button(root, text="Detached", command=self.detach_files, width=15)
        self.detach_button.pack(side=tk.LEFT, padx=(0, 5), pady=5)

        # Text area for displaying selected files
        self.text_area = tk.Text(root, height=5, state=tk.DISABLED)
        self.text_area.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Load JSON folder structure button
        self.load_button = tk.Button(root, text="Load JSON", command=self.load_json, width=15)
        self.load_button.pack(side=tk.RIGHT, padx=(5, 10), pady=5)

    def load_json(self):
        """
        Load JSON file and populate the tree view with folder structure.
        """
        filename = filedialog.askopenfilename(title="Select JSON file",
                                               filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        if filename:
            try:
                self.load_folder_structure(filename)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def load_folder_structure(self, filename):
        """
        Load folder structure from JSON file and populate the tree view.

        Parameters:
            filename (str): The path to the JSON file.
        """
        with open(filename, "r") as file:
            try:
                data = json.load(file)
                self.tree.delete(*self.tree.get_children())
                self.add_nodes("", data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON input in file: {filename}") from e

    def add_nodes(self, parent, data):
        """
        Recursively add nodes to the tree view.

        Parameters:
            parent (str): The parent node ID.
            data (dict): The folder structure data.
        """
        for key, value in data.items():
            if isinstance(value, dict):
                node = self.tree.insert(parent, "end", text=key)
                self.add_nodes(node, value)
            else:
                self.tree.insert(parent, "end", text=value)

    def on_tree_select(self, event):
        """
        Handle selection of tree view items.
        """
        selected_items = self.tree.selection()
        self.selected_files = [self.tree.item(item, "text") for item in selected_items]

    def attach_files(self):
        """
        Attach selected files to the text area.
        """
        if self.selected_files:
            self.text_area.config(state=tk.NORMAL)
            for file in self.selected_files:
                self.text_area.insert(tk.END, file + "\n")
            self.text_area.config(state=tk.DISABLED)

    def detach_files(self):
        """
        Clear the selected files from the text area.
        """
        self.selected_files = []
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)


if __name__ == "__main__":
    # Create and run the application
    root = tk.Tk()
    app = FolderExplorerApp(root)
    root.mainloop()
