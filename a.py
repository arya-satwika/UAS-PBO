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

    def filterTutors(self, matkul_filter="", waktu_filter="", search_query=""):
        result = []
        for tutor in self.tutors:
            match_matkul = (matkul_filter == "Semua") or (matkul_filter.lower() in ', '.join(tutor.get("mata-kuliah", [])).lower())
            match_waktu = (waktu_filter == "Semua") or (waktu_filter.lower() in tutor.get("waktu-belajar", "").lower())
            match_search = search_query.lower() in tutor.get("nama", "").lower()
            if match_matkul and match_waktu and match_search:
                result.append(tutor)
        return result

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

class ChatWindow(ctk.CTkToplevel):
    def __init__(self, master, tutor_nama):
        super().__init__(master)
        self.title(f"Chat dengan {tutor_nama}")
        self.geometry("400x400")

        label = ctk.CTkLabel(self, text=f"👋 Kamu sedang chatting dengan {tutor_nama}", font=("Helvetica", 16))
        label.pack(pady=20)

        self.textbox = ctk.CTkTextbox(self, width=350, height=250)
        self.textbox.pack(pady=10)

        self.entry = ctk.CTkEntry(self, width=300)
        self.entry.pack(side="left", padx=10, pady=10)

        self.send_button = ctk.CTkButton(self, text="Kirim", command=self.send_message)
        self.send_button.pack(side="right", padx=10)

    def send_message(self):
        message = self.entry.get()
        if message:
            self.textbox.insert("end", f"🧑 Kamu: {message}\n")
            self.entry.delete(0, "end")

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tutor Cerdas")
        self.geometry("1000x650")
        ctk.set_default_color_theme("green")

        self.search_query = ctk.StringVar()
        self.matkul_filter = ctk.StringVar()
        self.waktu_filter = ctk.StringVar()

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
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        # Ambil data unik untuk dropdown
        user = User()
        all_matkul = sorted({mk for tutor in user.tutors for mk in tutor.get("mata-kuliah", [])})
        all_waktu = sorted({tutor.get("waktu-belajar", "") for tutor in user.tutors})

        matkul_options = ["Semua"] + all_matkul
        waktu_options = ["Semua"] + all_waktu

        self.filter_bar = ctk.CTkFrame(container)
        self.filter_bar.pack(fill="x", padx=5, pady=(5, 10))

        search_entry = ctk.CTkEntry(self.filter_bar, placeholder_text="🔎 Cari Nama", textvariable=self.search_query, width=200)
        search_entry.pack(side="left", padx=10)

        self.matkul_filter.set("Semua")
        matkul_dropdown = ctk.CTkOptionMenu(self.filter_bar, values=matkul_options, variable=self.matkul_filter, width=180)
        matkul_dropdown.pack(side="left", padx=10)

        self.waktu_filter.set("Semua")
        waktu_dropdown = ctk.CTkOptionMenu(self.filter_bar, values=waktu_options, variable=self.waktu_filter, width=150)
        waktu_dropdown.pack(side="left", padx=10)

        filter_btn = ctk.CTkButton(self.filter_bar, text="Terapkan Filter", command=self.refresh_tutors)
        filter_btn.pack(side="left", padx=10)

        self.main_frame = ctk.CTkScrollableFrame(container, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True)

    def refresh_tutors(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tutor_obj = User()
        filtered = tutor_obj.filterTutors(
            matkul_filter=self.matkul_filter.get(),
            waktu_filter=self.waktu_filter.get(),
            search_query=self.search_query.get()
        )
        for tutor in filtered:
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

        chat_button = ctk.CTkButton(action_frame, text="💬 Chat", font=("Helvetica", 14), fg_color="#1f6f8b", hover_color="#145374", text_color="white", corner_radius=10, command=lambda: ChatWindow(self, tutor['nama']))
        chat_button.pack()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
