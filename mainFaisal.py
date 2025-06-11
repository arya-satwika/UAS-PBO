import customtkinter as ctk
from user import User
from chatwindow import ChatWindow
from registerTutor import RegisterTutor

class GUI(ctk.CTk):
    def __init__(self, user):
        self.user_instance = user
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
        self.status_label.configure(text=message)

    def refresh_tutors(self):
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
        RegisterTutor(self, self.user_instance)

    def open_chat(self, tutor_data):
        """Open chat window with specific tutor"""
        ChatWindow(self, tutor_data)

    

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
    gui= GUI(User())
    gui.run()