import customtkinter as ctk
from tkinter import messagebox
import json
import os

DATA_FILE = "data.json"
#heyo
def load_users():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"tutor": []}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=2)

class Tutor:
    def __init__(self, name, email, matkul):
        self.name = name
        self.email = email
        self.matkul = matkul

    def to_dict(self):
        return {"name": self.name, "email": self.email, "matkul": self.matkul}

class RegisterTutor:
    def __init__(self, master):
        self.master = master
        master.title("Register Pengajar")

        self.label_name = ctk.CTkLabel(master, text="Nama Pengajar:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(master)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_email = ctk.CTkLabel(master, text="Email:")
        self.label_email.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(master)
        self.entry_email.grid(row=1, column=1, padx=10, pady=5)

        self.label_matkul = ctk.CTkLabel(master, text="Mata Kuliah:")
        self.label_matkul.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_matkul = ctk.CTkEntry(master)
        self.entry_matkul.grid(row=2, column=1, padx=10, pady=5)

        self.button_register = ctk.CTkButton(master, text="Register", command=self.register_tutor)
        self.button_register.grid(row=3, column=0, columnspan=2, pady=10)

    def register_tutor(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        matkul = self.entry_matkul.get()

        if not name or not email or not matkul:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        tutor = Tutor(name, email, matkul)
        users = load_users()
        users["tutor"].append(tutor.to_dict())
        save_users(users)

        messagebox.showinfo("Sukses", f"Pengajar {tutor.name} berhasil didaftarkan!")
        self.entry_name.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_matkul.delete(0, ctk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    app = RegisterTutor(root)
    root.mainloop()



users = json.load(open("data.json"))

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.loadAllTutors()
    def loadAllTutors(self):
        user_list = users.get("tutor", [])
        return user_list
    def filterByMatkul(self, matkul):
        filtered_list = [
            filtered_user
            for filtered_user in users.get("tutor", [])
                if matkul in filtered_user.get("matkul", [])]
        return filtered_list
class matkul:
    def __init__(self, name, code):
        self.name = name
        self.code = code


