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

class User:
    def __init__(self, name, age, email=None, matkul=None):
        self.name = name
        self.age = age
        self.email = email
        self.matkul = matkul
        self.users = load_users()
        self.tutors = self.users.get("tutor", [])

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "matkul": self.matkul
        }

    def add_tutor(self):
        tutor_dict = self.to_dict()
        tutor_dict = {k: v for k, v in tutor_dict.items() if v is not None and k != "age"}
        self.tutors.append(tutor_dict)
        self.users["tutor"] = self.tutors
        save_users(self.users)

    def loadAllTutors(self):
        return self.tutors

    def filterByMatkul(self, matkul):
        filtered_list = [
            filtered_user
            for filtered_user in self.tutors
            if matkul in filtered_user.get("matkul", [])
        ]
        return filtered_list

class RegisterTutor:
    def __init__(self, master):
        self.master = master
        master.title("TutorCerdas")

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

        user = User(name, 0, email, matkul)
        user.add_tutor()

        messagebox.showinfo("Sukses", f"Pengajar {name} berhasil didaftarkan!")
        self.entry_name.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_matkul.delete(0, ctk.END)

if __name__ == "__main__":
    root = ctk.CTk()
    app = RegisterTutor(root)
    root.mainloop()

users = json.load(open("data.json"))

class matkul:
    def __init__(self, name, code):
        self.name = name
        self.code = code


