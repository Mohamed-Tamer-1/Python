import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import font as tkfont

class CustomSimpleDialog(simpledialog.Dialog):
    def __init__(self, parent, title, prompt, dialog_type="string"):
        self.prompt = prompt
        self.dialog_type = dialog_type
        super().__init__(parent, title)
    
    def body(self, master):
        tk.Label(master, text=self.prompt, font=tkfont.Font(size=14)).grid(row=0)
        if self.dialog_type == "string":
            self.entry = tk.Entry(master, font=tkfont.Font(size=14))
            self.entry.grid(row=1)
        elif self.dialog_type == "integer":
            self.entry = tk.Entry(master, font=tkfont.Font(size=14))
            self.entry.grid(row=1)
        return self.entry

    def apply(self):
        if self.dialog_type == "string":
            self.result = self.entry.get()
        elif self.dialog_type == "integer":
            self.result = int(self.entry.get())

def custom_askstring(title, prompt):
    dialog = CustomSimpleDialog(None, title, prompt, dialog_type="string")
    return dialog.result

def custom_askinteger(title, prompt):
    dialog = CustomSimpleDialog(None, title, prompt, dialog_type="integer")
    return dialog.result

def get_input():
    root = tk.Tk()
    root.withdraw()
    global url
    url = custom_askstring("URL", "Enter url:")
    if url is None:
        messagebox.showerror("Input Error", "No input provided for url.")
        root.destroy()
        return
    global epi
    epi = custom_askinteger("Episode", "Enter episodes:")
    if epi is None:
        messagebox.showerror("Input Error", "No input provided for episodes.")
        root.destroy()
        return