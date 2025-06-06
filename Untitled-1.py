import tkinter as tk
from tkinter import messagebox

class Tutor:
    def __init__(self, name, email, matkul):
        self.name = name
        self.email = email
        self.matkul = matkul

class RegisterTutorApp:
    def __init__(self, master):
        self.master = master
        master.title("Register Pengajar")

        self.label_name = tk.Label(master, text="Nama Pengajar:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_name = tk.Entry(master)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_email = tk.Label(master, text="Email:")
        self.label_email.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = tk.Entry(master)
        self.entry_email.grid(row=1, column=1, padx=10, pady=5)

        self.label_matkul = tk.Label(master, text="Mata Kuliah:")
        self.label_matkul.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_matkul = tk.Entry(master)
        self.entry_matkul.grid(row=2, column=1, padx=10, pady=5)

        self.button_register = tk.Button(master, text="Register", command=self.register_tutor)
        self.button_register.grid(row=3, column=0, columnspan=2, pady=10)

    def register_tutor(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        matkul = self.entry_matkul.get()

        if not name or not email or not matkul:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        tutor = Tutor(name, email, matkul)
        # Simpan ke database/file di sini jika diperlukan
        messagebox.showinfo("Sukses", f"Pengajar {tutor.name} berhasil didaftarkan!")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegisterTutorApp(root)
    root.mainloop()