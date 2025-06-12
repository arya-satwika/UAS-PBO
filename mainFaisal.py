import customtkinter as ctk
import tkinter.messagebox as mb
# ctk.set_appearance_mode("dark")
from theme import color_pallete
from user import User
from chatwindow import ChatWindow
from registerTutor import RegisterTutor
from GUIuser import UserProfile
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
        # Initialize user instance and current filter
        self.user_instance = User()
        self.user_instance.getUserByUsername("user3")
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
        title.pack(pady=20, padx=70)

        register_btn = ctk.CTkButton(
            sidebar, 
            text="Daftar Tutor",
            command=self.open_register_window,
            corner_radius=30,
            height=40,
            font=("Helvetica", 20, "bold"),
            text_color=color_pallete["text_clickable"],
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            )
        register_btn.pack(pady=10, padx=30, fill="x")

                # User profile section
        profile_frame = ctk.CTkFrame(
            sidebar,
            corner_radius=16,
            fg_color="transparent",
            # border_width=1,
        )
        profile_frame.pack(side="bottom", fill="x", padx=16, pady=16)

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

    def open_profile(self):
        UserProfile(self, self.user_instance)

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
        
        # # Search label
        # search_label = ctk.CTkLabel(
        #     self.search_frame,
        #     text="Cari:",
        #     font=("Helvetica", 14, "bold"),
        #     text_color="#333333"
        # )
        # search_label.grid(row=0, column=0, padx=(15, 10), pady=15, sticky="w")
        
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
        
        # # Filter label
        # filter_label = ctk.CTkLabel(
        #     self.search_frame,
        #     text="Filter:",
        #     font=("Helvetica", 14, "bold"),
        #     text_color="#333333"
        # )
        # filter_label.grid(row=0, column=2, padx=(10, 10), pady=15, sticky="w")
        
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