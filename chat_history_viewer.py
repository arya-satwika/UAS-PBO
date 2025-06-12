import customtkinter as ctk
import datetime
from theme import color_pallete

# Set consistent appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ChatHistoryViewer(ctk.CTkToplevel):
    def __init__(self, master, tutor_data):
        super().__init__(master)
        self.tutor_data = tutor_data
        self.title(f"Riwayat Chat - {tutor_data['nama']}")
        self.geometry("700x800")
        self.resizable(True, True)
        self.configure(fg_color=color_pallete["background"])
        self.grab_set()  # Make this window modal
        self.focus_set()
        
        # Center the window
        self.center_window()
        
        # Dummy chat history data
        self.chat_messages = [
            {
                "sender": "tutor",
                "message": "Halo! Saya siap membantu Anda belajar. Silakan tanyakan apa saja! 😊",
                "timestamp": "2024-01-15 14:30:15"
            },
            {
                "sender": "user",
                "message": "Halo pak, saya mau tanya tentang integral parsial",
                "timestamp": "2024-01-15 14:31:22"
            },
            {
                "sender": "tutor",
                "message": "Baik, integral parsial adalah teknik integrasi yang menggunakan rumus ∫u dv = uv - ∫v du. Mari kita bahas dengan contoh.",
                "timestamp": "2024-01-15 14:32:10"
            },
            {
                "sender": "user",
                "message": "Bisa kasih contoh soal pak?",
                "timestamp": "2024-01-15 14:33:05"
            },
            {
                "sender": "tutor",
                "message": "Tentu! Misalnya ∫x·e^x dx. Kita pilih u = x dan dv = e^x dx, sehingga du = dx dan v = e^x.",
                "timestamp": "2024-01-15 14:34:18"
            },
            {
                "sender": "user",
                "message": "Oh begitu, jadi hasilnya x·e^x - ∫e^x dx = x·e^x - e^x + C ya pak?",
                "timestamp": "2024-01-15 14:35:42"
            },
            {
                "sender": "tutor",
                "message": "Benar sekali! Bisa juga ditulis sebagai e^x(x-1) + C. Pemahaman Anda sudah bagus!",
                "timestamp": "2024-01-15 14:36:15"
            },
            {
                "sender": "user",
                "message": "Terima kasih pak! Sangat membantu penjelasannya",
                "timestamp": "2024-01-15 14:37:08"
            },
            {
                "sender": "tutor",
                "message": "Sama-sama! Jangan ragu untuk bertanya jika ada materi lain yang ingin dipelajari.",
                "timestamp": "2024-01-15 14:37:45"
            }
        ]
        
        self.setup_ui()
        self.load_chat_history()
    
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
        
        # Tutor info in header
        tutor_info = ctk.CTkLabel(
            header_frame,
            text=f"Riwayat Chat dengan {self.tutor_data['nama']}",
            font=("Helvetica", 18, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        tutor_info.grid(row=0, column=0, sticky="w", pady=(15,5), padx=(20, 0))
        
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
        close_btn.grid(row=0, column=1, padx=(10, 15), pady=(15,5), sticky="e")

        # Chat date info
        date_info = ctk.CTkLabel(
            header_frame,
            text=f"📅 Terakhir chat: {self.tutor_data['last_chat']} • {self.tutor_data['message_count']} pesan",
            font=("Helvetica", 11),
            text_color=color_pallete["text_secondary"]
        )
        date_info.grid(row=1, column=0, columnspan=2, pady=(0, 15), padx=20, sticky="w")
        
        # Chat area (scrollable) - same as ChatWindow but read-only
        self.chat_frame = ctk.CTkScrollableFrame(
            self, 
            corner_radius=15,
            fg_color=color_pallete["main_bg"],
            border_color=color_pallete["main_border"],
            border_width=1,
            scrollbar_fg_color="transparent",
            scrollbar_button_color=color_pallete["sidebar_border"]
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Disabled input frame (greyed out)
        input_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            border_width=1
        )
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Disabled message entry
        disabled_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Riwayat chat (hanya baca)",
            font=("Helvetica", 14),
            height=40,
            state="disabled",
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["text_secondary"],
            corner_radius=20
        )
        disabled_entry.grid(row=0, column=0, sticky="ew", padx=(15, 10), pady=15)
        
        # Disabled send button
        disabled_send_btn = ctk.CTkButton(
            input_frame,
            text="Kirim",
            width=80,
            height=40,
            state="disabled",
            fg_color=color_pallete["entry_bg"],
            text_color=color_pallete["text_secondary"],
            corner_radius=20,
            font=("Helvetica", 14, "bold")
        )
        disabled_send_btn.grid(row=0, column=1, padx=(0, 15), pady=15)
    
    def load_chat_history(self):
        """Load and display chat history"""
        for message_data in self.chat_messages:
            if message_data["sender"] == "user":
                self.add_user_message(message_data["message"], message_data["timestamp"])
            else:
                self.add_tutor_message(message_data["message"], message_data["timestamp"])
        
        # Scroll to bottom after loading all messages
        self.after(100, self.scroll_to_bottom)
    
    def add_user_message(self, message, timestamp):
        """Add user message to chat history"""
        # Message container
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.grid(sticky="ew", padx=5, pady=2)
        msg_container.grid_columnconfigure(0, weight=1)
        
        # Message frame (aligned to right)
        msg_frame = ctk.CTkFrame(
            msg_container, 
            fg_color=color_pallete["clickable_bg"], 
            corner_radius=15,
            border_color=color_pallete["clickable_border"],
            border_width=1
        )
        msg_frame.grid(row=0, column=1, sticky="e", padx=(50, 0))
        
        # Message text
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            text_color=color_pallete["text_clickable"],
            wraplength=300,
            justify="left"
        )
        msg_label.grid(padx=15, pady=10)
        
        # Timestamp
        time_str = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
        time_label = ctk.CTkLabel(
            msg_container,
            text=time_str,
            font=("Helvetica", 10),
            text_color=color_pallete["text_secondary"]
        )
        time_label.grid(row=1, column=1, sticky="e", padx=(0, 5))
    
    def add_tutor_message(self, message, timestamp):
        """Add tutor message to chat history"""
        # Message container
        msg_container = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        msg_container.grid(sticky="ew", padx=5, pady=2)
        msg_container.grid_columnconfigure(1, weight=1)
        
        # Message frame (aligned to left)
        msg_frame = ctk.CTkFrame(
            msg_container, 
            fg_color=color_pallete["card_bg"], 
            corner_radius=15,
            border_color=color_pallete["card_border"],
            border_width=1
        )
        msg_frame.grid(row=0, column=1, sticky="w", padx=(0, 50))
        
        # Message text
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=message,
            font=("Helvetica", 12),
            text_color=color_pallete["text_primary"],
            wraplength=300,
            justify="left"
        )
        msg_label.grid(padx=15, pady=10)
        
        # Timestamp
        time_str = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime("%H:%M")
        time_label = ctk.CTkLabel(
            msg_container,
            text=time_str,
            font=("Helvetica", 10),
            text_color=color_pallete["text_secondary"]
        )
        time_label.grid(row=1, column=1, sticky="w", padx=(5, 0))
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        self.chat_frame._parent_canvas.yview_moveto(1.0)

if __name__ == "__main__":
    app = ChatHistoryViewer(ctk.CTk(), {
        "nama": "Budi Santoso",
        "last_chat": "15 Januari 2024",
        "message_count": 8
    })
    app.mainloop()