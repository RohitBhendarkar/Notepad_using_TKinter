import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Notepad 1.0")
        self.root.geometry("800x600")

        # Current file being edited
        self.current_file = None

        self.create_menu()
        self.create_text_area()
        self.create_shortcuts()

        # Track changes for save prompt
        self.text_modified = False
        self.text_area.bind('<<Modified>>', self.on_modify)

    def create_menu(self):
        """Create the menu bar with all options"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut", command=lambda: self.text_area.event_generate("<<Cut>>"),
                              accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: self.text_area.event_generate("<<Copy>>"),
                              accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: self.text_area.event_generate("<<Paste>>"),
                              accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")

        # Help Menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_text_area(self):
        """Create the main text editing area"""
        # Create a frame to hold the text area and scrollbar
        self.text_frame = ttk.Frame(self.root)
        self.text_frame.pack(expand=True, fill='both')

        # Create the scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side='right', fill='y')

        # Create the text area
        self.text_area = tk.Text(
            self.text_frame,
            yscrollcommand=self.scrollbar.set,
            undo=True,
            wrap='word',
            font=('TkDefaultFont', 12)
        )
        self.text_area.pack(expand=True, fill='both')

        # Configure the scrollbar
        self.scrollbar.config(command=self.text_area.yview)

    def create_shortcuts(self):
        """Create keyboard shortcuts"""
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Control-x>', lambda e: self.text_area.event_generate("<<Cut>>"))
        self.root.bind('<Control-c>', lambda e: self.text_area.event_generate("<<Copy>>"))
        self.root.bind('<Control-v>', lambda e: self.text_area.event_generate("<<Paste>>"))
        self.root.bind('<Control-z>', lambda e: self.text_area.edit_undo())

    def on_modify(self, event):
        """Track if the text has been modified"""
        if self.text_area.edit_modified():
            self.text_modified = True
        self.text_area.edit_modified(False)

    def new_file(self):
        """Create a new file"""
        if self.text_modified:
            if not self.prompt_save_changes():
                return
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.text_modified = False
        self.root.title("Text Editor")

    def open_file(self):
        """Open an existing file"""
        if self.text_modified:
            if not self.prompt_save_changes():
                return

        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, file.read())
                    self.current_file = file_path
                    self.text_modified = False
                    self.root.title(f"Text Editor - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.text_modified = False
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """Save the file with a new name"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, tk.END))
                self.current_file = file_path
                self.text_modified = False
                self.root.title(f"Text Editor - {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {str(e)}")

    def select_all(self, event=None):
        """Select all text in the editor"""
        self.text_area.tag_add('sel', '1.0', 'end')
        return "break"

    def prompt_save_changes(self):
        """Prompt user to save changes before closing"""
        response = messagebox.askyesnocancel(
            "Save Changes?",
            "Do you want to save the changes before closing?"
        )

        if response is None:  # Cancel
            return False
        elif response:  # Yes
            self.save_file()
        return True

    def show_about(self):
        """Show the about dialog"""
        messagebox.showinfo(
            "About Text Editor",
            "Simple Text Editor\nCreated with Python and Tkinter\nVersion 1.0"
        )

    def exit_editor(self):
        """Exit the application"""
        if self.text_modified:
            if not self.prompt_save_changes():
                return
        self.root.quit()


def main():
    root = tk.Tk()
    editor = TextEditor(root)
    root.protocol("WM_DELETE_WINDOW", editor.exit_editor)
    root.mainloop()


if __name__ == "__main__":
    main()
