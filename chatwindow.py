import customtkinter as ctk
import os
import json
import random
import datetime
from theme import color_pallete

# Set consistent appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "tutor_responses.json")

try:
    responses = json.load(open(DATA_PATH))
except FileNotFoundError:
    print("File not found")
    responses = {"tutor_responses": ["Halo! Saya siap membantu Anda belajar. Silakan tanyakan apa saja! 😊"]}

class ChatWindow(ctk.CTkToplevel):
    def __init__(self, master, tutor_data):
        super().__init__(master)
        self.tutor_data = tutor_data
        self.title(f"Chat dengan {tutor_data['nama']}")
        self.geometry("600x500")
        self.resizable(True, True)
        self.configure(fg_color=color_pallete["background"])
        self.grab_set()  # Make this window modal
        self.focus_set()
        # Center the window
        self.center_window()
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        self.header_frame = ctk.CTkFrame(
            self, 
            corner_radius=25, 
            fg_color=color_pallete["card_bg"],
            border_color=color_pallete["card_border"],
            border_width=1
        )
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # # Tutor info in header
        # self.tutor_avatar = ctk.CTkLabel(
        #     self.header_frame,
        #     text="👨‍🏫",
        #     font=("Segoe UI", 24)
        # )
        # self.tutor_avatar.grid(row=0, column=0, padx=(15, 10), pady=10)
                
        self.tutor_info = ctk.CTkLabel(
            self.header_frame,
            text=f"{tutor_data['nama']}",
            font=("Helvetica", 20, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w",
            justify="left"
        )
        self.tutor_info.grid(row=0, column=1, sticky="w", pady=10, padx=(30, 0))
        
        # Close button
        self.close_btn = ctk.CTkButton(
            self.header_frame,
            text="❌",
            width=30,
            height=30,
            fg_color="transparent",
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            command=self.destroy
        )
        self.close_btn.grid(row=0, column=2, padx=(10, 15), pady=10)
        
        # Chat area (scrollable)
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
        
        # Message input frame
        self.input_frame = ctk.CTkFrame(
            self, 
            corner_radius=20,
            fg_color=color_pallete["highlight_bg"],
            border_color=color_pallete["highlight_border"],
            border_width=1
            
        )
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Message entry
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Ketik pesan Anda...",
            font=("Helvetica", 14),
            height=40,
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"]
        )
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(15, 10), pady=15)
        
        # Send button
        self.send_btn = ctk.CTkButton(
            self.input_frame,
            text="Kirim",
            width=80,
            height=40,
            fg_color=color_pallete["clickable_border"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            corner_radius=20,
            font=("Helvetica", 14, "bold"),
            command=self.send_message
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 15), pady=15)
        
        # Bind Enter key to send message
        self.message_entry.bind('<Return>', lambda event: self.send_message())
        
        # Focus on message entry
        self.message_entry.focus()
        
        # Add welcome message
        tutor_responses = responses.get("tutor_responses", [])
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
        timestamp = datetime.datetime.now().strftime("%H:%M")
        time_label = ctk.CTkLabel(
            msg_container,
            text=timestamp,
            font=("Helvetica", 10),
            text_color=color_pallete["text_secondary"]
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
        timestamp = datetime.datetime.now().strftime("%H:%M")
        time_label = ctk.CTkLabel(
            msg_container,
            text=timestamp,
            font=("Helvetica", 10),
            text_color=color_pallete["text_secondary"]
        )
        time_label.grid(row=1, column=1, sticky="w", padx=(5, 0))
        
        # Scroll to bottom
        self.after(100, self.scroll_to_bottom)
    
    def generate_tutor_reply(self):
        """Generate a random reply from the tutor."""
        tutor_responses = responses.get("tutor_responses", [])
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
