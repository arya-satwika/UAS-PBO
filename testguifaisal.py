import os
import json
import customtkinter as ctk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
users = json.load(open(DATA_PATH))

class User:
    def __init__(self):
        self.tutors = self.loadAllTutors()

    def loadAllTutors(self):
        return users.get("tutor", [])

    def filterByMatkul(self, matkul):
        return [u for u in self.tutors if matkul in u.get("mata-kuliah", [])]

class RegisterTutor(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Daftar Pengajar")
        self.geometry("400x300")

        self.label_name = ctk.CTkLabel(self, text="Nama Pengajar:")
        self.label_name.pack(pady=5)
        self.entry_name = ctk.CTkEntry(self)
        self.entry_name.pack(pady=5)

        self.label_email = ctk.CTkLabel(self, text="Email:")
        self.label_email.pack(pady=5)
        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.pack(pady=5)

        self.label_matkul = ctk.CTkLabel(self, text="Mata Kuliah:")
        self.label_matkul.pack(pady=5)
        self.entry_matkul = ctk.CTkEntry(self)
        self.entry_matkul.pack(pady=5)

        self.button_register = ctk.CTkButton(self, text="Register", command=self.register_tutor)
        self.button_register.pack(pady=20)

    def register_tutor(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        matkul = self.entry_matkul.get()

        if not name or not email or not matkul:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        users["tutor"].append({
            "nama": name,
            "email": email,
            "mata-kuliah": [matkul],
            "waktu-belajar": "Senin-Jumat",
            "tempat-belajar": "Online"
        })

        with open(DATA_PATH, 'w') as f:
            json.dump(users, f, indent=4)

        messagebox.showinfo("Sukses", f"Pengajar {name} berhasil didaftarkan!")
        self.destroy()

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tutor Cerdas")
        self.geometry("950x600")
        ctk.set_default_color_theme("green")

        self.sidebar()
        self.main_area()
        self.refresh_tutors()

    def sidebar(self):
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=15)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        title = ctk.CTkLabel(sidebar, text="📚 Tutor Cerdas", font=("Helvetica", 20, "bold"))
        title.pack(pady=20)

        register_btn = ctk.CTkButton(sidebar, text="➕ Daftarkan Tutor", command=self.open_register_window)
        register_btn.pack(pady=10)

    def main_area(self):
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh_tutors(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tutors = User().loadAllTutors()
        for tutor in tutors:
            self.tutor_card(tutor)

    def open_register_window(self):
        RegisterTutor(self)

    def tutor_card(self, tutor):
        card = ctk.CTkFrame(self.main_frame, fg_color="#ffffff", corner_radius=20, border_width=1, border_color="#d1d1d1")
        card.pack(pady=10, padx=20, fill="x", expand=True)

        nama_label = ctk.CTkLabel(card, text=f"👤 {tutor['nama']}", font=("Helvetica", 22, "bold"), text_color="#333333")
        nama_label.pack(anchor="w", padx=20, pady=(10, 5))

        matkul_label = ctk.CTkLabel(card, text=f"📘 Mata Kuliah: {', '.join(tutor['mata-kuliah'])}", font=("Helvetica", 16), text_color="#555555")
        matkul_label.pack(anchor="w", padx=20)

        detail_label = ctk.CTkLabel(card, text=f"⏰ {tutor['waktu-belajar']}   📍 {tutor['tempat-belajar']}", font=("Helvetica", 15), text_color="#666666")
        detail_label.pack(anchor="w", padx=20, pady=(5, 10))

        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(anchor="e", padx=20, pady=(0, 10))

        chat_button = ctk.CTkButton(action_frame, text="💬 Chat", font=("Helvetica", 14), fg_color="#1f6f8b", hover_color="#145374", text_color="white", corner_radius=10, command=lambda: print(f"Chat with {tutor['nama']}"))
        chat_button.pack()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
