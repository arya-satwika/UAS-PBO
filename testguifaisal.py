import os
import json
import customtkinter as ctk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

# Load users data
try:
    users = json.load(open(DATA_PATH))
except FileNotFoundError:
    users = {"tutor": [], "admin": [{"username": "admin", "password": "admin123"}]}
    with open(DATA_PATH, 'w') as f:
        json.dump(users, f, indent=4)

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

class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - Tutor Cerdas")
        self.geometry("600x500")
        ctk.set_default_color_theme("green")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.main_container = ctk.CTkFrame(self, corner_radius=20, fg_color="#ffffff", border_width=2, border_color="#d1d1d1")
        self.main_container.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="📚 Tutor Cerdas", 
            font=("Helvetica", 28, "bold"),
            text_color="#1f6f8b"
        )
        self.title_label.grid(row=0, column=0, pady=(30, 10))
        self.subtitle_label = ctk.CTkLabel(
            self.main_container, 
            text="Masuk ke akun Anda", 
            font=("Helvetica", 16),
            text_color="#666666"
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30))
        self.username_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.username_frame.grid(row=2, column=0, sticky="ew", padx=40)
        self.username_frame.grid_columnconfigure(0, weight=1)
        self.username_label = ctk.CTkLabel(
            self.username_frame, 
            text="👤 Username:", 
            font=("Helvetica", 14, "bold"),
            text_color="#333333",
            anchor="w"
        )
        self.username_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            placeholder_text="Masukkan username",
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            border_width=2,
            border_color="#d1d1d1"
        )
        self.username_entry.grid(row=1, column=0, sticky="ew")
        self.password_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.password_frame.grid(row=3, column=0, sticky="ew", padx=40, pady=(20, 0))
        self.password_frame.grid_columnconfigure(0, weight=1)
        self.password_label = ctk.CTkLabel(
            self.password_frame, 
            text="🔒 Password:", 
            font=("Helvetica", 14, "bold"),
            text_color="#333333",
            anchor="w"
        )
        self.password_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Masukkan password",
            show="*",
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            border_width=2,
            border_color="#d1d1d1"
        )
        self.password_entry.grid(row=1, column=0, sticky="ew")
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=40, pady=(30, 0))
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.login_button = ctk.CTkButton(
            self.button_frame,
            text="🚀 Masuk",
            font=("Helvetica", 16, "bold"),
            height=45,
            corner_radius=15,
            fg_color="#1f6f8b",
            hover_color="#145374",
            command=self.login
        )
        self.login_button.grid(row=0, column=0, sticky="ew")
        self.bind('<Return>', lambda event: self.login())
        self.username_entry.focus()
        self.after(100, self.center_window)
    
    def center_window(self):
        """Center the window on screen after ensuring it's fully rendered"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        # Check admin credentials
        admin_users = users.get("admin", [])
        for admin in admin_users:
            if admin.get("username") == username and admin.get("password") == password:
                messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
                self.open_main_app()
                return
        
        # Check users credentials
        user_users = users.get("users", [])
        for user in user_users:
            if user.get("username") == username and user.get("password") == password:
                messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
                self.open_main_app()
                return
        
        # Check tutor credentials (using email as username, no password check)
        tutor_users = users.get("tutor", [])
        for tutor in tutor_users:
            if tutor.get("email") == username:
                messagebox.showinfo("Sukses", f"Selamat datang, {tutor.get('nama')}!")
                self.open_main_app()
                return
        
        messagebox.showerror("Error", "Username atau password salah!")
        self.password_entry.delete(0, 'end')
    
    def open_register(self, event=None):
        """Open registration window"""
        RegisterTutor(self)
    
    def open_main_app(self):
        """Open main application and close login window"""
        self.destroy()
        main_app = GUI()
        main_app.run()

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
        
        # Logout button
        logout_btn = ctk.CTkButton(
            sidebar, 
            text="🚪 Logout", 
            fg_color="#dc3545", 
            hover_color="#c82333",
            command=self.logout
        )
        logout_btn.pack(side="bottom", pady=20)

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

    def logout(self):
        """Logout and return to login page"""
        result = messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?")
        if result:
            self.destroy()
            login_app = LoginPage()
            login_app.mainloop()

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
    # Start with login page
    login_app = LoginPage()
    login_app.mainloop()