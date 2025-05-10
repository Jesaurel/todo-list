import tkinter as tk
from tkinter import messagebox

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title="Input", prompt="Masukkan teks:"):
        super().__init__(parent)
        self.title(title)
        self.configure(bg="#1E1E1E")
        self.resizable(False, False)

        self.result = None

        tk.Label(self, text=prompt, font=("Poppins", 12), bg="#1E1E1E", fg="#D1D1D1").pack(pady=10)
        
        self.entry = tk.Entry(self, font=("Poppins", 12), width=30, bg="#2B2B2B", fg="white", bd=0, insertbackground="white")
        self.entry.pack(pady=5, padx=20, fill="x")
        self.entry.focus()
        
        btn_frame = tk.Frame(self, bg="#1E1E1E")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="OK", font=("Poppins", 12, "bold"), bg="#3A7D44", fg="white", width=10, command=self.confirm).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Batal", font=("Poppins", 12, "bold"), bg="#D9534F", fg="white", width=10, command=self.cancel).pack(side="right", padx=5)

        self.grab_set()

    def confirm(self):
        self.result = self.entry.get()
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark To-Do List")
        self.root.configure(bg="#121212")
        
        self.header = tk.Frame(self.root, bg="#1E1E1E", height=60)
        self.header.grid(row=0, column=0, sticky="ew") # Changed to grid
        tk.Label(self.header, text="To-Do List", font=("Poppins", 18, "bold"), bg="#1E1E1E", fg="white").pack(side="left", padx=20, pady=15)
        
        self.add_button = tk.Button(self.header, text="+", font=("Poppins", 16, "bold"), bg="#3A7D44", fg="white", width=3, bd=0, relief="flat", command=self.add_task_popup)
        self.add_button.pack(side="right", padx=20)

        self.task_frame = tk.Frame(self.root, bg="#121212")
        self.task_frame.grid(row=1, column=0, sticky="nsew") # Changed to grid

        # Placeholder jika tidak ada tugas
        self.placeholder_label = tk.Label(self.task_frame, text="Belum ada tugas", font=("Poppins", 14, "italic"), fg="#888888", bg="#121212")
        self.placeholder_label.pack(pady=20)

        # Tombol Hapus Semua
        self.clear_all_button = tk.Button(self.root, text="Hapus Semua", font=("Poppins", 12, "bold"), bg="#D9534F", fg="white", bd=0, relief="flat", command=self.clear_all_tasks)
        self.clear_all_button.grid(row=2, column=0, sticky="s") # Changed to grid
        self.clear_all_button.pack_forget()

        self.tasks = []
        
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

    def add_task_popup(self):
        dialog = CustomDialog(self.root, "Tambah Tugas", "Masukkan tugas baru:")
        self.root.wait_window(dialog)
        if dialog.result:
            self.add_task(dialog.result)

    def add_task(self, task_text):
        task_frame = tk.Frame(self.task_frame, bg="#2B2B2B", bd=2, relief="groove")
        task_frame.pack(pady=5, padx=10, fill="x")
        
        task_label = tk.Label(task_frame, text=task_text, font=("Poppins", 12), bg="#2B2B2B", fg="white", wraplength=400)
        task_label.pack(side="left", padx=10, fill="x", expand=True)
        
        edit_button = tk.Button(task_frame, text="✏️", font=("Poppins", 12, "bold"), bg="#3A7D44", fg="white", bd=0, relief="flat", command=lambda: self.edit_task(task_label))
        edit_button.pack(side="right", padx=5)
        
        delete_button = tk.Button(task_frame, text="🗑", font=("Poppins", 12, "bold"), bg="#D9534F", fg="white", bd=0, relief="flat", command=lambda: self.delete_task(task_frame))
        delete_button.pack(side="right", padx=5)
        
        complete_button = tk.Button(task_frame, text="✔", font=("Poppins", 12, "bold"), bg="#4CAF50", fg="white", bd=0, relief="flat", command=lambda: self.complete_task(task_label))
        complete_button.pack(side="right", padx=5)
        
        self.tasks.append(task_frame)
        self.placeholder_label.pack_forget()
        self.update_clear_button()

    def edit_task(self, task_label):
        dialog = CustomDialog(self.root, "Edit Tugas", "Edit tugas:")
        dialog.entry.insert(0, task_label.cget("text"))
        self.root.wait_window(dialog)
        if dialog.result:
            task_label.config(text=dialog.result)
    
    def complete_task(self, task_label):
        task_label.config(fg="#A0A0A0", font=("Poppins", 12, "overstrike"))  
    
    def delete_task(self, task_frame):
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus tugas ini?")
        if confirm:
            task_frame.destroy()
            self.tasks.remove(task_frame)
            self.update_clear_button()

    def clear_all_tasks(self):
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua tugas?")
        if confirm:
            for task in self.tasks:
                task.destroy()
            self.tasks.clear()
            self.update_clear_button()

    def update_clear_button(self):
        if self.tasks:
            self.clear_all_button.pack(pady=10)
        else:
            self.clear_all_button.pack_forget()
            self.placeholder_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
        
