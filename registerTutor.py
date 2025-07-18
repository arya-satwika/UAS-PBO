import customtkinter as ctk
from tkinter import messagebox

from user import User, Tutor
from theme import color_pallete

# Set consistent appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RegisterTutor(ctk.CTkToplevel):
    def __init__(self, master, user):
        super().__init__(master)
        self.title("Daftar Pengajar")
        self.geometry("600x700")
        self.resizable(False, False)
        self.current_user = user
        self.tutor_instance = Tutor()
        self.configure(fg_color=color_pallete["background"])
        self.grab_set()  # Make this window modal
        self.focus_set()
        # Center the window
        self.center_window()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        if self.current_user.role == "pengajar":
            messagebox.showinfo("Info", "Anda sudah terdaftar sebagai pengajar.")
            self.destroy()
            return
            
        # Main container
        self.main_container = ctk.CTkFrame(
            self, 
            corner_radius=20, 
            fg_color=color_pallete["card_bg"], 
            border_width=2, 
            border_color=color_pallete["card_border"]
        )
        self.main_container.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="👨‍🏫 Daftar Pengajar", 
            font=("Helvetica", 24, "bold"),
            text_color=color_pallete["text_primary"]
        )
        self.title_label.grid(row=0, column=0, pady=(20, 30))
        
        # Name field
        self.name_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.name_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 15))
        self.name_frame.grid_columnconfigure(0, weight=1)
        
        self.name_label = ctk.CTkLabel(
            self.name_frame, 
            text=f"👤 {self.current_user.username} Mendaftar sebagai pengajar!", 
            font=("Helvetica", 20, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        self.name_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        # Harga field
        self.harga_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.harga_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 15))
        self.harga_frame.grid_columnconfigure(0, weight=1)
        
        self.harga_label = ctk.CTkLabel(
            self.harga_frame, 
            text="💰 Harga :", 
            font=("Helvetica", 14, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        self.harga_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.harga_entry = ctk.CTkEntry(
            self.harga_frame,
            placeholder_text="Contoh: 19000",
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=color_pallete["entry_border"],
            fg_color=color_pallete["entry_bg"],
            text_color=color_pallete["entry_text"]
        )
        self.harga_entry.grid(row=1, column=0, sticky="ew")

        # Mata Kuliah field
        self.matkul_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.matkul_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(0, 15))
        self.matkul_frame.grid_columnconfigure(0, weight=1)
        
        self.matkul_label = ctk.CTkLabel(
            self.matkul_frame, 
            text="📚 Mata Kuliah:", 
            font=("Helvetica", 14, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        self.matkul_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.matkul_entry = ctk.CTkEntry(
            self.matkul_frame,
            placeholder_text="Contoh: Pemrograman Dasar, Struktur Data",
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=color_pallete["entry_border"],
            fg_color=color_pallete["entry_bg"],
            text_color=color_pallete["entry_text"]
        )
        self.matkul_entry.grid(row=1, column=0, sticky="ew")

        # Waktu Belajar field
        self.waktu_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.waktu_frame.grid(row=4, column=0, sticky="ew", padx=30, pady=(0, 15))
        self.waktu_frame.grid_columnconfigure(0, weight=1)
        
        self.waktu_label = ctk.CTkLabel(
            self.waktu_frame, 
            text="⏰ Waktu Belajar:", 
            font=("Helvetica", 14, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        self.waktu_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.waktu_entry = ctk.CTkEntry(
            self.waktu_frame,
            placeholder_text="Contoh: Senin-Jumat 09:00-17:00",
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=color_pallete["entry_border"],
            fg_color=color_pallete["entry_bg"],
            text_color=color_pallete["entry_text"]
        )
        self.waktu_entry.grid(row=1, column=0, sticky="ew")
        
        # Tempat Belajar field
        self.tempat_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.tempat_frame.grid(row=5, column=0, sticky="ew", padx=30, pady=(0, 30))
        self.tempat_frame.grid_columnconfigure(0, weight=1)
        
        self.tempat_label = ctk.CTkLabel(
            self.tempat_frame, 
            text="📍 Tempat Belajar:", 
            font=("Helvetica", 14, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        self.tempat_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.tempat_entry = ctk.CTkEntry(
            self.tempat_frame,
            placeholder_text="Contoh: Online, Gedung A9, FC Ketintang",
            font=("Helvetica", 14),
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=color_pallete["entry_border"],
            fg_color=color_pallete["entry_bg"],
            text_color=color_pallete["entry_text"]
        )
        self.tempat_entry.grid(row=1, column=0, sticky="ew")
        
        # Button container
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.button_frame.grid(row=6, column=0, sticky="ew", padx=30, pady=(0, 20))
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Register button
        self.register_button = ctk.CTkButton(
            self.button_frame,
            text="✅ Daftar",
            font=("Helvetica", 16, "bold"),
            height=45,
            corner_radius=15,
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            command=self.register_tutor
        )
        self.register_button.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            self.button_frame,
            text="❌ Batal",
            font=("Helvetica", 16, "bold"),
            height=45,
            corner_radius=15,
            fg_color=color_pallete["error"],
            hover_color="#c82333",
            text_color=color_pallete["text_clickable"],
            command=self.destroy
        )
        self.cancel_button.grid(row=0, column=1, sticky="ew", padx=(10, 0))
        
        # Bind Enter key to register
        self.bind('<Return>', lambda event: self.register_tutor())

    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def register_tutor(self):
        # Convert mata kuliah input (comma separated) to a list of course names
        matkul_input = self.matkul_entry.get()
        matkul_list = [m.strip() for m in matkul_input.split(",") if m.strip()]

        data = {
            "nama": self.current_user.username,
            "prodi": self.current_user.prodi,
            "angkatan": self.current_user.angkatan,
            "harga": self.harga_entry.get(),
            "mata-kuliah": matkul_list,
            "waktu-belajar": self.waktu_entry.get(),
            "tempat-belajar": self.tempat_entry.get()
        }
        if self.tutor_instance.addUserToJson(data):

            self.current_user.role = "tutor"
            self.current_user.updateJson()
            messagebox.showinfo("Sukses", f"Pengajar {self.current_user.username} berhasil didaftarkan!")
            self.destroy()
        else:
            messagebox.showerror("Gagal", "Gagal mendaftarkan pengajar. Silakan coba lagi.")
