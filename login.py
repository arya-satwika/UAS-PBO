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

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login - TutorCerdas")
        self.geometry("500x600")
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
            text="Login",
            font=ctk.CTkFont(size=34, family="Helvetica", weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        title_label.grid(row=0, column=0, pady=(50, 50))
        
        # Form frame
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=1, column=0, sticky="ew", padx=40)
        form_frame.grid_columnconfigure(0, weight=1)
        
        # Username field
        username_label = ctk.CTkLabel(
            form_frame,
            text="Username:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        username_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Masukkan username Anda",
            placeholder_text_color=color_pallete["text_secondary_teal"],
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"],
            corner_radius=20
        )
        self.username_entry.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
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
        
        # Login button
        self.login_button = ctk.CTkButton(
            form_frame,
            text="Login",
            height=50,
            font=ctk.CTkFont(size=24, family="Helvetica", weight="bold"),
            command=self.handle_login,
            corner_radius=25,
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color=color_pallete["clickable_border"],
            border_width=1
        )
        self.login_button.grid(row=4, column=0, sticky="ew", pady=(10, 20))
        
        # Register link
        register_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        register_frame.grid(row=5, column=0, pady=(10, 30))
        
        register_text = ctk.CTkLabel(
            register_frame,
            text="Belum punya akun?",
            font=ctk.CTkFont(size=12),
            text_color=color_pallete["text_secondary"]
        )
        register_text.pack(side="left")
        
        register_button = ctk.CTkButton(
            register_frame,
            text="Daftar di sini",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="transparent",
            text_color=color_pallete["text_secondary_teal"],
            hover_color=color_pallete["highlight_bg"],
            width=80,
            height=20,
            command=self.open_register
        )
        register_button.pack(side="left", padx=(5, 0))
        
        # Bind Enter key to login
        self.bind('<Return>', lambda event: self.handle_login())
    
    def handle_login(self):
        """Handle login attempt"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        user = User()
        if user.authUser(username, password):
            messagebox.showinfo("Success", f"Selamat datang, {username}!")
            self.destroy()
            # Open main application with the logged in user
            user.getUserByUsername(username)
            GUI(user).mainloop()
        else:
            messagebox.showerror("Error", "Username atau password salah!")
            self.password_entry.delete(0, 'end')
    
    def open_register(self):
        """Open registration window"""
        from register_user import StudentRegister
        self.destroy()
        StudentRegister().mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()