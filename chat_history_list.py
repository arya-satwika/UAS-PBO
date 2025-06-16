import customtkinter as ctk
from theme import color_pallete
from chat_history_viewer import ChatHistoryViewer

# Set consistent appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ChatHistoryList(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Riwayat Chat")
        self.geometry("700x800")
        self.resizable(True, True)
        self.configure(fg_color=color_pallete["background"])
        self.grab_set()  # Make this window modal
        self.focus_set()
        
        # Center the window
        self.center_window()
        
        # Dummy data for tutors the user has chatted with
        self.chat_history_data = [
            {
                "nama": "Astuti",
                "mata-kuliah": ["Matematika", "Fisika"],
                "last_chat": "2024-01-15 14:30",
                "message_count": 25,
                "avatar": "👨‍🏫"
            },
            {
                "nama": "Prof. Siti Nurhaliza",
                "mata-kuliah": ["Kimia", "Biologi"],
                "last_chat": "2024-01-14 10:15",
                "message_count": 18,
                "avatar": "👩‍🏫"
            },
            {
                "nama": "Ir. Budi Prasetyo",
                "mata-kuliah": ["Pemrograman", "Algoritma"],
                "last_chat": "2024-01-13 16:45",
                "message_count": 42,
                "avatar": "👨‍💻"
            },
            {
                "nama": "Dr. Maya Sari",
                "mata-kuliah": ["Bahasa Inggris", "Sastra"],
                "last_chat": "2024-01-12 09:20",
                "message_count": 12,
                "avatar": "👩‍🏫"
            },
            {
                "nama": "Prof. Andi Wijaya",
                "mata-kuliah": ["Ekonomi", "Manajemen"],
                "last_chat": "2024-01-11 13:10",
                "message_count": 31,
                "avatar": "👨‍💼"
            }
        ]
        
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
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        header_frame = ctk.CTkFrame(
            self, 
            corner_radius=25, 
            fg_color=color_pallete["card_bg"],
            border_color=color_pallete["card_border"],
            border_width=1
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="💬 Riwayat Chat",
            font=("Helvetica", 20, "bold"),
            text_color=color_pallete["text_primary"]
        )
        title_label.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=(20, 0))

        # Close button
        close_btn = ctk.CTkButton(
            header_frame,
            text="❌",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            command=self.destroy
        )
        close_btn.grid(row=0, column=1, padx=(10, 15), pady=(10,5), sticky="e")
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Pilih tutor untuk melihat riwayat percakapan",
            font=("Helvetica", 12),
            text_color=color_pallete["text_secondary"]
        )
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 10), padx=20, sticky="w")
        
        # Scrollable frame for tutor list
        self.tutors_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=15,
            fg_color=color_pallete["main_bg"],
            border_color=color_pallete["main_border"],
            border_width=1,
            scrollbar_fg_color="transparent",
            scrollbar_button_color=color_pallete["sidebar_border"]
        )
        self.tutors_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Display tutor cards
        self.display_tutors()
    
    def display_tutors(self):
        """Display all tutors the user has chatted with"""
        if not self.chat_history_data:
            # Show no chat history message
            no_history_label = ctk.CTkLabel(
                self.tutors_frame,
                text="📭 Belum ada riwayat chat\n\nMulai chat dengan tutor untuk melihat riwayat di sini",
                font=("Helvetica", 16),
                text_color=color_pallete["text_secondary"],
                justify="center"
            )
            no_history_label.pack(pady=50)
        else:
            # Display tutor cards
            for tutor in self.chat_history_data:
                self.create_tutor_card(tutor)
    
    def create_tutor_card(self, tutor):
        """Create a card for each tutor in chat history"""
        card = ctk.CTkFrame(
            self.tutors_frame,
            fg_color=color_pallete["card_bg"],
            border_color=color_pallete["card_border"],
            corner_radius=20,
            border_width=1,
        )
        card.pack(pady=8, padx=10, fill="x")
        
        # Configure grid for card content
        card.grid_columnconfigure(1, weight=1)
        
        # Avatar
        avatar_label = ctk.CTkLabel(
            card,
            text=tutor["avatar"],
            font=("Helvetica", 32)
        )
        avatar_label.grid(row=0, column=0, rowspan=3, padx=(20, 15), pady=20)
        
        # Tutor name
        name_label = ctk.CTkLabel(
            card,
            text=tutor["nama"],
            font=("Gotham", 22, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", pady=(20, 3))
        
        # Subjects
        subjects_label = ctk.CTkLabel(
            card,
            text=f"Matkul: {', '.join(tutor['mata-kuliah'])}",
            font=("Helvetica", 12),
            text_color=color_pallete["text_secondary"],
            anchor="w"
        )
        subjects_label.grid(row=1, column=1, sticky="w", pady=2)
        
        # Last chat info
        info_text = f"💬 {tutor['message_count']} pesan • Terakhir: {tutor['last_chat']}"
        info_label = ctk.CTkLabel(
            card,
            text=info_text,
            font=("Helvetica", 12),
            text_color=color_pallete["text_secondary"],
            anchor="w"
        )
        info_label.grid(row=2, column=1, sticky="w", pady=(2, 20))
        
        # View chat button
        view_btn = ctk.CTkButton(
            card,
            text="Lihat Chat",
            width=120,
            height=50,
            font=("Helvetica", 18, "bold"),
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            corner_radius=25,
            command=lambda t=tutor: self.open_chat_history(t)
        )
        view_btn.grid(row=0, column=2, rowspan=3, padx=(10, 20), pady=20)
    
    def open_chat_history(self, tutor):
        """Open chat history viewer for selected tutor"""
        ChatHistoryViewer(self, tutor)
if __name__ == "__main__":
    app = ctk.CTk()
    app.withdraw()  # Hide the main window
    chat_history_list = ChatHistoryList(app)
    chat_history_list.mainloop()
    app.destroy()  # Clean up after closing the chat history list