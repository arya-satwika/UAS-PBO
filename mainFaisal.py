import customtkinter as ctk
import tkinter.messagebox as mb
# ctk.set_appearance_mode("dark")
from theme import color_pallete
from user import User
from chatwindow import ChatWindow
from registerTutor import RegisterTutor
from GUIuser import UserProfile
from chat_history_list import ChatHistoryList
# from register_user import StudentRegister

class GUI(ctk.CTk):
    def __init__(self, user):
        self.user_instance = user
        super().__init__()
        self.title("Tutor Cerdas")
        self.geometry("1100x700")
        ctk.set_default_color_theme("blue") 
        self.resizable(True, True)
        self.configure(fg_color=color_pallete["background"])
        self.center_window()
        ctk.deactivate_automatic_dpi_awareness()       
        ctk.set_window_scaling(1.0)  # Set scaling to 100%
        # Dummy data for recent messages
        self.recent_messages = [
            {
                "student_name": "Andi Wijaya",
                "last_message": "Halo pak, saya ingin belajar tentang kalkulus.",
                "timestamp": "14:30",
                "unread": True,
                "avatar": "👨‍🎓",
                "messages": [
                    {
                        "sender": "student",
                        "message": "Halo pak, saya ingin belajar tentang kalkulus. Apakah bapak bisa membantu?",
                        "timestamp": "2024-01-15 14:30:15"
                    }
                ]
            },
            {
                "student_name": "Budi Santoso",
                "last_message": "Selamat siang pak, saya mau konsultasi tentang mekanika kuantum.",
                "timestamp": "13:45",
                "unread": True,
                "avatar": "👨‍🎓",
                "messages": [
                    {
                        "sender": "student",
                        "message": "Selamat siang pak, saya mau konsultasi tentang materi mekanika kuantum.",
                        "timestamp": "2024-01-15 13:45:22"
                    }
                ]
            },
            {
                "student_name": "Citra Dewi",
                "last_message": "Pak, saya kesulitan memahami materi ikatan kimia.",
                "timestamp": "11:20",
                "unread": True,
                "avatar": "👩‍🎓",
                "messages": [
                    {
                        "sender": "student",
                        "message": "Pak, saya kesulitan memahami materi ikatan kimia. Bisakah bapak menjelaskan?",
                        "timestamp": "2024-01-15 11:20:05"
                    }
                ]
            },
            {
                "student_name": "Dian Purnama",
                "last_message": "Terima kasih atas penjelasannya pak!",
                "timestamp": "Kemarin",
                "unread": False,
                "avatar": "👩‍🎓",
                "messages": [
                    {
                        "sender": "student",
                        "message": "Terima kasih atas penjelasannya pak!",
                        "timestamp": "2024-01-14 16:20:05"
                    }
                ]
            },
            {
                "student_name": "Eko Prasetyo",
                "last_message": "Kapan kita bisa jadwalkan sesi berikutnya?",
                "timestamp": "Kemarin",
                "unread": False,
                "avatar": "👨‍🎓",
                "messages": [
                    {
                        "sender": "student",
                        "message": "Kapan kita bisa jadwalkan sesi berikutnya?",
                        "timestamp": "2024-01-14 15:10:05"
                    }
                ]
            }
        ]
        
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
    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def sidebar(self):
        sidebar = ctk.CTkFrame(
            self,
            width=300,
            corner_radius=35,
            fg_color=color_pallete["sidebar_fill"],
            border_color=color_pallete["sidebar_border"],
            border_width=1, 
            )
        sidebar.pack(side="left", fill="y", padx=(20,5), pady=20)

        title = ctk.CTkLabel(
            sidebar, 
            text="Tutorly",
            font=("Helvetica", 40, "bold"),
            text_color=color_pallete["text_secondary"]
            )
        title.pack(pady=(20, 10), padx=70)

        register_btn = ctk.CTkButton(
            sidebar, 
            text="Daftar Tutor",
            command=self.open_register_window,
            corner_radius=30,
            height=35,
            font=("Helvetica", 20, "bold"),
            text_color=color_pallete["text_clickable"],
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            )
        register_btn.pack(pady=5, padx=30, fill="x")

        # Chat History button
        chat_history_btn = ctk.CTkButton(
            sidebar, 
            text="💬 Riwayat Chat",
            command=self.open_chat_history,
            corner_radius=30,
            height=40,
            font=("Helvetica", 20, "bold"),
            text_color=color_pallete["text_clickable"],
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            )
        chat_history_btn.pack(pady=10, padx=30, fill="x")
        
        # Recent messages section (only for tutors)
        if hasattr(self.user_instance, 'role') and self.user_instance.role == "tutor":
            # Recent messages title
            recent_messages_title = ctk.CTkLabel(
                sidebar,
                text="Pesan Terbaru",
                font=("Helvetica", 16, "bold"),
                text_color=color_pallete["text_primary"]
            )
            recent_messages_title.pack(pady=(5, 10), padx=20, anchor="w")
            
            # Recent messages scrollable frame
            recent_messages_frame = ctk.CTkScrollableFrame(
                sidebar,
                height=20,
                fg_color=color_pallete["highlight_bg"],
                border_color=color_pallete["highlight_border"],
                border_width=1,
                corner_radius=15,
                scrollbar_fg_color="transparent",
                scrollbar_button_color=color_pallete["sidebar_border"]
            )
            recent_messages_frame.pack(padx=15, pady=(0, 5))
            
            # Add recent messages
            for message in self.recent_messages:
                self.create_message_item(recent_messages_frame, message)

        # Top Tutors section
        top_tutors_frame = ctk.CTkFrame(
            sidebar,
            corner_radius=20,
            fg_color=color_pallete["highlight_bg"],
            border_color=color_pallete["highlight_border"],
            border_width=1,
        )
        top_tutors_frame.pack(side="top", fill="x", padx=25, pady=(0, 8))

        # Top tutors title
        top_tutors_title = ctk.CTkLabel(
            top_tutors_frame,
            text="Tutor Terbaik",
            font=("Helvetica", 16, "bold"),
            text_color=color_pallete["text_primary"]
        )
        top_tutors_title.pack(pady=(15, 10))

        # Dummy data for top 3 tutors
        top_tutors = [
            {"nama": "Dr. Ahmad Santoso", "rating": 4.9},
            {"nama": "Prof. Siti Nurhaliza", "rating": 4.8},
            {"nama": "Ir. Budi Prasetyo", "rating": 4.7}
        ]

        # Display top 3 tutors
        for i, tutor in enumerate(top_tutors, 1):
            tutor_label = ctk.CTkLabel(
                top_tutors_frame,
                text=f"{i}. {tutor['nama']}",
                font=("Helvetica", 12),
                text_color=color_pallete["text_secondary"],
                anchor="w"
            )
            tutor_label.pack(pady=2, padx=15, fill="x")

        # Add some bottom padding
        ctk.CTkLabel(top_tutors_frame, text="", height=10).pack()

        # User profile section
        profile_frame = ctk.CTkFrame(
            sidebar,
            corner_radius=16,
            fg_color="transparent",
        )
        profile_frame.pack(side="bottom", fill="x", padx=16, pady=(0, 16))

        profile_label = ctk.CTkButton(
            profile_frame,
            text=f"👤 {self.user_instance.username}",
            font=("Segoe UI", 16, "bold"),
            text_color=color_pallete["text_primary"],
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            corner_radius=25,
            height=50,
            width=250,
            command=lambda: self.open_profile()
        )
        profile_label.pack(pady=5)
    
    def create_message_item(self, parent, message):
        """Create a message item in the recent messages list"""
        # Message frame
        message_frame = ctk.CTkFrame(
            parent,
            fg_color=color_pallete["card_bg"] if not message["unread"] else color_pallete["clickable_bg"],
            corner_radius=10,
            border_width=1,
            border_color=color_pallete["card_border"] if not message["unread"] else color_pallete["clickable_border"]
        )
        message_frame.pack(fill="x", padx=5, pady=5)
        
        # Make the entire frame clickable
        message_frame.bind("<Button-1>", lambda e, m=message: self.open_student_chat(m))
        
        # Configure grid
        message_frame.grid_columnconfigure(1, weight=0)
        
        # Student name
        name_label = ctk.CTkLabel(
            message_frame,
            text=message["student_name"],
            font=("Helvetica", 12, "bold"),
            text_color=color_pallete["text_primary"],
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=5, pady=(5, 0))
        
        # Last message (truncated)
        last_message = message["last_message"]
        if len(last_message) > 25:
            last_message = last_message[:25] + "..."
            
        message_label = ctk.CTkLabel(
            message_frame,
            text=last_message,
            font=("Helvetica", 10),
            text_color=color_pallete["text_secondary"],
            anchor="w"
        )
        message_label.grid(row=1, column=1, sticky="w", padx=5, pady=(0, 10))
        
        # Timestamp
        time_label = ctk.CTkLabel(
            message_frame,
            text=message["timestamp"],
            font=("Helvetica", 9),
            text_color=color_pallete["text_secondary"],
            anchor="e"
        )
        time_label.grid(row=0, column=2, padx=10, pady=(5, 0))
        
        # Unread indicator
        if message["unread"]:
            unread_indicator = ctk.CTkLabel(
                message_frame,
                text="●",
                font=("Helvetica", 12),
                text_color=color_pallete["success"],
                anchor="e"
            )
            unread_indicator.grid(row=1, column=2, padx=10, pady=(0, 10))
    
    def open_student_chat(self, message_data):
        """Open chat window with the student"""
        # Create a tutor-like data structure for the ChatWindow
        student_data = {
            "nama": message_data["student_name"],
            "mata-kuliah": ["Matematika", "Fisika"],  # Dummy data
            "messages": message_data["messages"]
        }
        
        # Open chat window
        ChatWindow(self, student_data)

    def open_profile(self):
        UserProfile(self, self.user_instance)

    def open_chat_history(self):
        """Open chat history list window"""
        ChatHistoryList(self)

    def main_area(self):
        # Main content container
        self.content_container = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.content_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Search and filter section
        self.search_frame = ctk.CTkFrame(
            self.content_container,
            corner_radius=25,
            fg_color=color_pallete["highlight_bg"],
            border_color=color_pallete["highlight_border"],
            border_width=1,
            )
        self.search_frame.pack(fill="x", padx=(5,15), pady=(15,10))
        
        # Configure grid for search frame
        self.search_frame.grid_columnconfigure(1, weight=1)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search",
            placeholder_text_color=color_pallete["text_secondary_teal"],
            font=("Helvetica", 14),
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            corner_radius=25,
            height=35
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(20, 10), pady=15)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Filter dropdown
        self.filter_var = ctk.StringVar(value="Filter")
        
        # Create dropdown options with "Filter" as first option
        dropdown_options = ["Filter"] + self.all_matkul
        
        self.filter_dropdown = ctk.CTkOptionMenu(
            self.search_frame,
            values=dropdown_options,
            variable=self.filter_var,   
            width=200,
            height=35,
            font=("Helvetica", 14),
            text_color=color_pallete["text_clickable"],
            dropdown_text_color=color_pallete["text_clickable"],
            dropdown_font=("Helvetica", 14),
            fg_color=color_pallete["clickable_bg"],
            dropdown_fg_color=color_pallete["clickable_bg"],
            dropdown_hover_color= color_pallete["clickable_border"],
            button_color=color_pallete["clickable_bg"],
            button_hover_color=color_pallete["clickable_border"],
            corner_radius=20,
            command=self.on_filter_change
        )
        self.filter_dropdown.grid(row=0, column=3, padx=(0, 15), pady=15, sticky="e")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.content_container,
            text="",
            font=("Helvetica", 14, "italic"),
            text_color=color_pallete["text_secondary"],
        )
        self.status_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        # Tutors display area (scrollable)
        
        self.main_frame = ctk.CTkScrollableFrame(
            self.content_container,
            corner_radius=25,
            fg_color=color_pallete["main_bg"],
            border_color=color_pallete["main_border"],
            border_width=1,
            scrollbar_fg_color="transparent",
            scrollbar_button_color=color_pallete["sidebar_border"],
            scrollbar_button_hover_color=color_pallete["sidebar_border"],
        )
        self.main_frame.pack(expand=True, fill="both", padx=(5,15), pady=(0, 15))
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
        if choice == "Filter":
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
        self.status_label.configure(text=message)

    def refresh_tutors(self):
        # Reset filter dropdown
        self.filter_var.set("Filter")
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
        RegisterTutor(self, self.user_instance)

    def open_chat(self, tutor_data):
        """Open chat window with specific tutor"""
        ChatWindow(self, tutor_data)

    
    def popup_bayar(self, tutor):
        result = mb.askyesno(
            "Konfirmasi Pembayaran",
            f"Anda akan membayar {tutor['harga']} ke {tutor['nama']}\nLanjutkan pembayaran?"
        )
        if result:
            self.user_instance.transfer_ke_tutor(tutor)
            self.open_chat(tutor)
    def tutor_card(self, tutor):
        card = ctk.CTkFrame(
            self.main_frame,
            fg_color=color_pallete["card_bg"],
            border_color=color_pallete["card_border"],
            corner_radius=25,
            border_width=1,
        )
        card.pack(pady=10, padx=(5, 15), fill="x", expand=True)

        nama_label = ctk.CTkLabel(
            card,
            text=f"👤 {tutor['nama']}",
            font=("Helvetica", 34, "bold"),
            text_color=color_pallete["text_primary"]
        )
        nama_label.pack(anchor="w", padx=20, pady=20)

        matkul_label = ctk.CTkLabel(
            card,
            text=f"Mata Kuliah: {', '.join(tutor['mata-kuliah'])}", 
            text_color=color_pallete["text_secondary_teal"],
            wraplength=550,
            justify="left",
            font=("Helvetica", 20),
        )   
        matkul_label.pack(anchor="w", padx=20)

        action_frame = ctk.CTkFrame(card, fg_color="transparent")
        action_frame.pack(side="bottom", padx=5, pady=(0, 10), fill="x")

        detail_label = ctk.CTkLabel(
            action_frame,
            text=f"⏰ {tutor['waktu-belajar']}\n📍 {tutor['tempat-belajar']}",
            text_color=color_pallete["text_secondary"],
            font=("Segoe UI", 15),
        )
        detail_label.pack(anchor="w", padx=15, pady=20)

        harga_frame = ctk.CTkFrame(
            action_frame,
            width=200,
            height=20,
            fg_color="transparent"
        )
        harga_frame.pack(padx=10, anchor="e")
        harga_formatted = f"{tutor['harga']:,}".replace(",", ".")
        harga_frame.propagate(False)  # Prevent frame from resizing to fit content
        harga_label = ctk.CTkLabel(
            harga_frame,
            text=f"Rp. {harga_formatted}",
            text_color=color_pallete["text_secondary"],
            font=("Segoe UI", 14),
        )
        harga_label.pack(anchor="center")
        chat_button = ctk.CTkButton(
            action_frame,
            text="💬 Chat",
            text_color=color_pallete["text_clickable"],
            font=("Segoe UI", 20, "bold"),
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            corner_radius=30,
            height=50,
            width=200,
            command=lambda:self.popup_bayar(tutor)
        )
        chat_button.pack(padx=10,pady=(5,10), side="right")
        chat_button.propagate(False)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    gui= GUI(User())
    gui.run()
