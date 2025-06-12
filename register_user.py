import os
import json
import customtkinter as ctk
from tkinter import messagebox
from theme import color_pallete
from user import User
from mainFaisal import GUI

# Set consistent appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class StudentRegister(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.user_instance = User()
        # Configure window
        self.title("Registrasi Mahasiswa - TutorCerdas")
        self.geometry("500x750")
        self.resizable(False, False)
        self.configure(fg_color=color_pallete["background"])
        
        # Center the window
        self.center_window()
        
        # File paths
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.DATA_PATH = os.path.join(self.BASE_DIR, "data.json")
        # Setup UI
        self.setup_ui()
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main frame
        main_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            fg_color=color_pallete["sidebar_fill"],
            border_color=color_pallete["sidebar_border"],
            border_width=1
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Registrasi",
            font=ctk.CTkFont(size=34, family="Helvetica", weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        title_label.grid(row=0, column=0, pady=(50, 50))
        
        # Form frame
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=2, column=0, sticky="ew", padx=40)
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Name field
        name_label = ctk.CTkLabel(
            form_frame,
            text="Nama Lengkap:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        name_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Masukkan nama lengkap Anda",
            placeholder_text_color=color_pallete["text_secondary_teal"],
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"],
            corner_radius=20
        )
        self.name_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Password field
        password_label = ctk.CTkLabel(
            form_frame,
            text="Password:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        password_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Masukkan password",
            placeholder_text_color=color_pallete["text_secondary_teal"],
            height=40,
            font=ctk.CTkFont(size=14),
            show="*",
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"],
            corner_radius=20
        )
        self.password_entry.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        # Program Studi field
        prodi_label = ctk.CTkLabel(
            form_frame,
            text="Program Studi:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        prodi_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        # Prodi dropdown
        prodi_options = [
            "Teknik Informatika",
            "Sistem Informasi", 
            "Pendidikan Teknologi Informasi",
            "Teknik Komputer",
            "Desain Komunikasi Visual",
            "Hukum",
            "Manajemen",
            "Akuntansi",
            "Lainnya"
        ]
        
        self.prodi_combobox = ctk.CTkComboBox(
            form_frame,
            values=prodi_options,
            height=40,
            font=ctk.CTkFont(size=14, family="Helvetica"),
            dropdown_font=ctk.CTkFont(size=12, family="Helvetica"),
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"],
            button_color=color_pallete["entry_border"],
            button_hover_color=color_pallete["clickable_border"],
            dropdown_fg_color=color_pallete["entry_bg"],
            dropdown_hover_color=color_pallete["entry_border"],
            dropdown_text_color=color_pallete["text_primary"],
            corner_radius=20
        )
        self.prodi_combobox.grid(row=5, column=0, sticky="ew", pady=(0, 20))
        self.prodi_combobox.set("Pilih Program Studi")
        
        # Angkatan field
        angkatan_label = ctk.CTkLabel(
            form_frame,
            text="Angkatan:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        angkatan_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        # Angkatan dropdown
        current_year = 2024
        angkatan_options = [str(year) for year in range(current_year, current_year-10, -1)]
        
        self.angkatan_combobox = ctk.CTkComboBox(
            form_frame,
            values=angkatan_options,
            height=40,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=12),
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"],
            button_color=color_pallete["entry_border"],
            button_hover_color=color_pallete["clickable_border"],
            dropdown_fg_color=color_pallete["clickable_bg"],
            dropdown_hover_color=color_pallete["clickable_border"],
            dropdown_text_color=color_pallete["text_primary"],
            corner_radius=20

        )
        self.angkatan_combobox.grid(row=7, column=0, sticky="ew", pady=(0, 30))
        self.angkatan_combobox.set("Pilih Tahun Angkatan")
        
        # Register button
        self.register_button = ctk.CTkButton(
            form_frame,
            text="Daftar",
            height=50,
            font=ctk.CTkFont(size=24, family="Helvetica", weight="bold"),
            command=self.register_student,
            corner_radius=25,
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color=color_pallete["clickable_border"],
            border_width=1
            
        )
        self.register_button.grid(row=8, column=0, sticky="ew", pady=(10, 20))
        
        # Login link
        login_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        login_frame.grid(row=9, column=0, pady=(10, 30))
        
        login_text = ctk.CTkLabel(
            login_frame,
            text="Sudah punya akun?",
            font=ctk.CTkFont(size=12),
            text_color=color_pallete["text_secondary"]
        )
        login_text.pack(side="left")
        
        login_button = ctk.CTkButton(
            login_frame,
            text="Login di sini",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            text_color=color_pallete["text_secondary_teal"],
            hover_color=color_pallete["highlight_bg"],
            width=80,
            height=20,
            command=self.open_login
        )
        login_button.pack(side="left", padx=(5, 0))
    
    def validate_input(self):
        """Validate all input fields"""
        name = self.name_entry.get().strip()
        password = self.password_entry.get().strip()
        prodi = self.prodi_combobox.get()
        angkatan = self.angkatan_combobox.get()
        
        if not name:
            messagebox.showerror("Error", "Nama lengkap harus diisi!")
            return False
        
        if len(name) < 2:
            messagebox.showerror("Error", "Nama harus minimal 2 karakter!")
            return False
        
        if not password:
            messagebox.showerror("Error", "Password harus diisi!")
            return False
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password harus minimal 6 karakter!")
            return False
        
        if prodi == "Pilih Program Studi":
            messagebox.showerror("Error", "Program Studi harus dipilih!")
            return False
        
        if angkatan == "Pilih Tahun Angkatan":
            messagebox.showerror("Error", "Tahun Angkatan harus dipilih!")
            return False
        
        return True
    
    
    def register_student(self):
        """Register new student"""
        if not self.validate_input():
            return
        
        name = self.name_entry.get().strip()
        password = self.password_entry.get().strip()
        prodi = self.prodi_combobox.get()
        angkatan = self.angkatan_combobox.get()
        
        # Disable button during registration
        self.register_button.configure(state="disabled", text="Mendaftar...")
        
        try:
            # Create new student data
            student_data = {
                "username": name,
                "password": password,
                "angkatan": angkatan,
                "prodi": prodi,
                "saldo": 0,
                "role": "student"
            }
            if self.user_instance.addUserToJson(student_data) is not True:
                messagebox.showerror("Error", "Terjadi kesalahan saat mendaftar.")
                return
            # Show success message
            messagebox.showinfo(
                "Berhasil!", 
                f"Selamat {name}!\n\nAkun mahasiswa Anda berhasil didaftarkan.\n"
                f"Program Studi: {prodi}\n"
                f"Angkatan: {angkatan}\n"
                f"Saldo Awal: Rp 0\n\n"
                "Silakan login untuk mulai menggunakan layanan tutor."
            )
            # Clear form
            self.clear_form()

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat mendaftar: {str(e)}")
        
        finally:
            # Re-enable button
            self.register_button.configure(state="normal", text="Daftar Sekarang")
            self.user_instance= User()
            self.user_instance.getUserByUsername(name)  # Load user data
            self.destroy()
            GUI(self.user_instance).mainloop()  # Transition to main GUI
    def clear_form(self):
        """Clear all form fields"""
        self.name_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.prodi_combobox.set("Pilih Program Studi")
        self.angkatan_combobox.set("Pilih Tahun Angkatan")
    
    def open_login(self):
        """Open login window (placeholder)"""
        messagebox.showinfo("Info", "Fitur login akan segera tersedia!")

if __name__ == "__main__":
    app = StudentRegister()
    app.mainloop()