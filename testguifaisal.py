import os
import json
import customtkinter as ctk
from tkinter import messagebox
import random
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")

# Load users data
try:
    users = json.load(open(DATA_PATH))
except FileNotFoundError:
    users = {"tutor": [], "admin": [{"username": "admin", "password": "admin123"}], "students": []}
    with open(DATA_PATH, 'w') as f:
        json.dump(users, f, indent=4)

# Global variable to store current user info
current_user = {"username": "", "type": "", "data": {}}

class User:
    def __init__(self):
        self.tutors = self.loadAllTutors()

    def loadAllTutors(self):
        return users.get("tutor", [])

    def filterByMatkul(self, matkul):
        return [u for u in self.tutors if matkul in u.get("mata-kuliah", [])]

class ChatWindow(ctk.CTkToplevel):
    def __init__(self, master, tutor_data):
        super().__init__(master)
        self.tutor_data = tutor_data
        self.title(f"Chat dengan {tutor_data['nama']}")
        self.geometry("600x500")
        self.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        self.header_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1f6f8b")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Tutor info in header
        self.tutor_avatar = ctk.CTkLabel(
            self.header_frame,
            text="👨‍🏫",
            font=("Helvetica", 24)
        )
        self.tutor_avatar.grid(row=0, column=0, padx=(15, 10), pady=10)
        
        self.tutor_info = ctk.CTkLabel(
            self.header_frame,
            text=f"{tutor_data['nama']}\n📚 {', '.join(tutor_data['mata-kuliah'])}",
            font=("Helvetica", 14, "bold"),
            text_color="white",
            anchor="w",
            justify="left"
        )
        self.tutor_info.grid(row=0, column=1, sticky="w", pady=10)
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self.header_frame,
            text="❌",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color="#145374",
            command=self.destroy
        )
        self.close_btn.grid(row=0, column=2, padx=(10, 15), pady=10)
        
        # Chat area (scrollable)
        self.chat_frame = ctk.CTkScrollableFrame(self, corner_radius=15)
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Message input frame
        self.input_frame = ctk.CTkFrame(self, corner_radius=15)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Message entry
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ketik pesan Anda...",
            font=("Helvetica", 14),
            height=40
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(15, 10), pady=15)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="📤 Kirim",
            width=80,
            height=40,
            fg_color="#1f6f8b",
            hover_color="#145374",
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 15), pady=15)
        
        # Bind Enter key to send message
        self.message_entry.bind('<Return>', lambda event: self.send_message())
        
        # Focus on message entry
        self.message_entry.focus()
        
        # Add welcome message
        tutor_responses = users.get("tutor_responses", [])
        if tutor_responses:
            welcome_message = tutor_responses[0]
        else:
            welcome_message = "Halo! Saya siap membantu Anda belajar. Silakan tanyakan apa saja! 😊"
        self.add_tutor_message(welcome_message)
    
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def send_message(self):
        """Send user message and get tutor reply"""
        message = self.message_entry.get().strip()
        if not message:
            return
        
        # Add user message
        self.add_user_message(message)
        
        # Clear input
        self.message_entry.delete(0, 'end')
        
        # Generate tutor reply after a short delay
        self.after(1000, self.generate_tutor_reply)
    
    def add_user_message(self, message):
        """Add user message to chat"""
        # Message container
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.grid(sticky="ew", padx=5, pady=2)
        msg_container.grid_columnconfigure(0, weight=1)
        
        # Message frame (aligned to right)
        msg_frame = ctk.CTkFrame(msg_container, fg_color="#1f6f8b", corner_radius=15)
        msg_frame.grid(row=0, column=1, sticky="e", padx=(50, 0))
        
        # Message text
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            text_color="white",
            wraplength=300,
            justify="left"
        )
        msg_label.grid(padx=15, pady=10)
        
        # Timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M")
        time_label = ctk.CTkLabel(
            msg_container,
            text=timestamp,
            font=("Helvetica", 10),
            text_color="#666666"
        )
        time_label.grid(row=1, column=1, sticky="e", padx=(0, 5))
        
        # Scroll to bottom
        self.after(100, self.scroll_to_bottom)
    
    def add_tutor_message(self, message):
        """Add tutor message to chat"""
        # Message container
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.grid(sticky="ew", padx=5, pady=2)
        msg_container.grid_columnconfigure(1, weight=1)
        
        # Avatar
        avatar_label = ctk.CTkLabel(
            msg_container,
            text="👨‍🏫",
            font=("Helvetica", 16)
        )
        avatar_label.grid(row=0, column=0, sticky="n", padx=(0, 10), pady=(5, 0))
        
        # Message frame (aligned to left)
        msg_frame = ctk.CTkFrame(msg_container, fg_color="#f0f0f0", corner_radius=15)
        msg_frame.grid(row=0, column=1, sticky="w", padx=(0, 50))
        
        # Message text
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            text_color="#333333",
            wraplength=300,
            justify="left"
        )
        msg_label.grid(padx=15, pady=10)
        
        # Timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M")
        time_label = ctk.CTkLabel(
            msg_container,
            text=timestamp,
            font=("Helvetica", 10),
            text_color="#666666"
        )
        time_label.grid(row=1, column=1, sticky="w", padx=(5, 0))
        
        # Scroll to bottom
        self.after(100, self.scroll_to_bottom)
    
    def generate_tutor_reply(self):
        """Generate a random reply from the tutor."""
        tutor_responses = users.get("tutor_responses", [])
        if len(tutor_responses) > 1:
            reply = random.choice(tutor_responses[1:])
        elif tutor_responses:
            reply = tutor_responses[0]
        else:
            reply = "Maaf, saya tidak mengerti."
        self.add_tutor_message(reply)
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        self.chat_frame._parent_canvas.yview_moveto(1.0)

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
        self.geometry("600x550")
        ctk.set_default_color_theme("green")
        
        # Configure grid for responsive layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container with padding
        self.main_container = ctk.CTkFrame(self, corner_radius=20, fg_color="#ffffff", border_width=2, border_color="#d1d1d1")
        self.main_container.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")
        
        # Configure main container grid
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_container, 
            text="📚 Tutor Cerdas", 
            font=("Helvetica", 28, "bold"),
            text_color="#1f6f8b"
        )
        self.title_label.grid(row=0, column=0, pady=(30, 10))
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.main_container, 
            text="Masuk ke akun Anda", 
            font=("Helvetica", 16),
            text_color="#666666"
        )
        self.subtitle_label.grid(row=1, column=0, pady=(0, 30))
        
        # Username field container
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
        
        # Password field container
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
        
        # Button container
        self.button_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, sticky="ew", padx=40, pady=(30, 0))
        self.button_frame.grid_columnconfigure(0, weight=1)
        
        # Login button
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
        
        # Register tutor link
        self.register_label = ctk.CTkLabel(
            self.main_container,
            text="Ingin mengajar? Daftar sebagai tutor",
            font=("Helvetica", 12),
            text_color="#1f6f8b",
            cursor="hand2"
        )
        self.register_label.grid(row=5, column=0, pady=(20, 30))
        self.register_label.bind("<Button-1>", self.open_tutor_register)
        
        # Bind Enter key to login
        self.bind('<Return>', lambda event: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
        
        # Center window after all widgets are added
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
        global current_user
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Username dan password harus diisi!")
            return
        
        student_users = users.get("users", [])
        for student in student_users:
            if student.get("username") == username and student.get("password") == password:
                current_user = {
                    "username": username,
                    "type": "student",
                    "data": student
                }
                messagebox.showinfo("Sukses", f"Selamat datang, {username}!")
                self.open_main_app()
                return
        
        # Check tutor credentials (using email as username)
        tutor_users = users.get("tutor", [])
        for tutor in tutor_users:
            if tutor.get("email") == username:
                current_user = {
                    "username": tutor.get("nama", username),
                    "type": "tutor",
                    "data": tutor
                }
                messagebox.showinfo("Sukses", f"Selamat datang, {tutor.get('nama')}!")
                self.open_main_app()
                return
        
        messagebox.showerror("Error", "Username atau password salah!")
        self.password_entry.delete(0, 'end')
    
    def open_tutor_register(self, event=None):
        """Open tutor registration window"""
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
        
        # Initialize user instance and current filter
        self.user_instance = User()
        self.current_filter = None
        self.current_tutors = self.user_instance.loadAllTutors()
        
        # Get all unique mata kuliah for dropdown
        self.all_matkul = set()
        for tutor in self.user_instance.loadAllTutors():
            self.all_matkul.update(tutor.get("mata-kuliah", []))
        self.all_matkul = sorted(list(self.all_matkul))

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
        
        # Bottom section frame for logout
        bottom_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # Logout button
        logout_btn = ctk.CTkButton(
            bottom_frame, 
            text="🚪 Logout", 
            fg_color="#dc3545", 
            hover_color="#c82333",
            height=35,
            command=self.logout
        )
        logout_btn.pack(fill="x")

    def main_area(self):
        # Main content container
        self.content_container = ctk.CTkFrame(self, corner_radius=15)
        self.content_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Search and filter section
        self.search_frame = ctk.CTkFrame(self.content_container, corner_radius=15, fg_color="#f8f9fa")
        self.search_frame.pack(fill="x", padx=15, pady=15)
        
        # Configure grid for search frame
        self.search_frame.grid_columnconfigure(1, weight=1)
        
        # Search label
        search_label = ctk.CTkLabel(
            self.search_frame,
            text="🔍 Cari:",
            font=("Helvetica", 14, "bold"),
            text_color="#333333"
        )
        search_label.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="w")
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Cari berdasarkan nama tutor...",
            font=("Helvetica", 14),
            height=35
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=15)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Filter label
        filter_label = ctk.CTkLabel(
            self.search_frame,
            text="📚 Filter:",
            font=("Helvetica", 14, "bold"),
            text_color="#333333"
        )
        filter_label.grid(row=0, column=2, padx=(10, 10), pady=15, sticky="w")
        
        # Filter dropdown
        self.filter_var = ctk.StringVar(value="Semua Mata Kuliah")
        
        # Create dropdown options with "Semua Mata Kuliah" as first option
        dropdown_options = ["Semua Mata Kuliah"] + self.all_matkul
        
        self.filter_dropdown = ctk.CTkOptionMenu(
            self.search_frame,
            values=dropdown_options,
            variable=self.filter_var,
            width=200,
            height=35,
            font=("Helvetica", 14),
            dropdown_font=("Helvetica", 14),
            fg_color="#1f6f8b",
            button_color="#1f6f8b",
            button_hover_color="#145374",
            command=self.on_filter_change
        )
        self.filter_dropdown.grid(row=0, column=3, padx=(0, 15), pady=15, sticky="e")
        
        # Search button
        search_btn = ctk.CTkButton(
            self.search_frame,
            text="🔍",
            width=40,
            height=35,
            fg_color="#1f6f8b",
            hover_color="#145374",
            command=self.search_tutors
        )
        search_btn.grid(row=0, column=4, padx=(0, 15), pady=15)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.content_container,
            text="",
            font=("Helvetica", 12),
            text_color="#666666"
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        # Tutors display area (scrollable)
        self.main_frame = ctk.CTkScrollableFrame(self.content_container, corner_radius=15)
        self.main_frame.pack(expand=True, fill="both", padx=15, pady=(0, 15))

    def on_search_change(self, event=None):
        """Handle search as user types"""
        search_term = self.search_entry.get().strip().lower()
        if search_term:
            self.search_tutors()
        else:
            # If search is empty, show current filter or all tutors
            self.apply_current_filter()

    def on_filter_change(self, choice):
        """Handle filter dropdown change"""
        if choice == "Semua Mata Kuliah":
            self.current_filter = None
        else:
            self.current_filter = choice
        
        self.apply_current_filter()
    
    def apply_current_filter(self):
        """Apply the current filter and search term"""
        search_term = self.search_entry.get().strip().lower()
        
        if self.current_filter:
            # Filter by mata kuliah
            filtered_tutors = self.user_instance.filterByMatkul(self.current_filter)
            self.current_tutors = filtered_tutors
            
            # Apply search if there's a search term
            if search_term:
                filtered_tutors = [t for t in filtered_tutors if search_term in t.get("nama", "").lower()]
            
            self.display_tutors(filtered_tutors)
            
            # Update status
            if filtered_tutors:
                status_text = f"Menampilkan {len(filtered_tutors)} tutor untuk mata kuliah '{self.current_filter}'"
            else:
                status_text = f"Tidak ada tutor untuk mata kuliah '{self.current_filter}'"
            
            self.show_status_message(status_text)
        else:
            # Show all tutors
            all_tutors = self.user_instance.loadAllTutors()
            self.current_tutors = all_tutors
            
            # Apply search if there's a search term
            if search_term:
                all_tutors = [t for t in all_tutors if search_term in t.get("nama", "").lower()]
            
            self.display_tutors(all_tutors)
            
            # Update status
            status_text = f"Menampilkan semua {len(all_tutors)} tutor"
            self.show_status_message(status_text)

    def search_tutors(self):
        """Search tutors by name"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            # If search is empty, show current filter or all tutors
            self.apply_current_filter()
            return
        
        # Filter tutors by name
        filtered_tutors = []
        base_tutors = self.current_tutors if self.current_filter else self.user_instance.loadAllTutors()
        
        for tutor in base_tutors:
            if search_term in tutor.get("nama", "").lower():
                filtered_tutors.append(tutor)
        
        self.display_tutors(filtered_tutors)
        
        # Update status
        if filtered_tutors:
            status_text = f"Ditemukan {len(filtered_tutors)} tutor dengan nama '{search_term}'"
        else:
            status_text = f"Tidak ada tutor dengan nama '{search_term}'"
        
        self.show_status_message(status_text)

    def display_tutors(self, tutors):
        """Display the given list of tutors"""
        # Clear existing tutor cards
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        if not tutors:
            # Show no results message
            no_results_label = ctk.CTkLabel(
                self.main_frame,
                text="😔 Tidak ada tutor yang ditemukan",
                font=("Helvetica", 18),
                text_color="#666666"
            )
            no_results_label.pack(pady=50)
        else:
            # Display tutor cards
            for tutor in tutors:
                self.tutor_card(tutor)

    def show_status_message(self, message):
        """Show status message in the status label"""
        self.status_label.configure(text=message)

    def refresh_tutors(self):
        """Refresh the tutor display"""
        # Reset filter dropdown
        self.filter_var.set("Semua Mata Kuliah")
        self.current_filter = None
        
        # Clear search
        self.search_entry.delete(0, 'end')
        
        # Show all tutors
        all_tutors = self.user_instance.loadAllTutors()
        self.current_tutors = all_tutors
        self.display_tutors(all_tutors)
        
        # Update status
        status_text = f"Menampilkan semua {len(all_tutors)} tutor"
        self.show_status_message(status_text)

    def open_register_window(self):
        RegisterTutor(self)

    def open_chat(self, tutor_data):
        """Open chat window with specific tutor"""
        ChatWindow(self, tutor_data)

    def logout(self):
        """Logout and return to login page"""
        global current_user
        result = messagebox.askyesno("Logout", "Apakah Anda yakin ingin logout?")
        if result:
            current_user = {"username": "", "type": "", "data": {}}
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

        chat_button = ctk.CTkButton(
            action_frame, 
            text="💬 Chat", 
            font=("Helvetica", 14), 
            fg_color="#1f6f8b", 
            hover_color="#145374", 
            text_color="white", 
            corner_radius=10, 
            command=lambda: self.open_chat(tutor)
        )
        chat_button.pack()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    # Start with login page
    login_app = LoginPage()
    login_app.mainloop()