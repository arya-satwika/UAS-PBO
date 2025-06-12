import customtkinter as ctk
# Enable dark mode
ctk.set_appearance_mode("dark")
from user import User
from chatwindow import ChatWindow
from registerTutor import RegisterTutor

class GUI(ctk.CTk):
    def __init__(self, user):
        self.user_instance = user
        super().__init__()
        self.title("Tutor Cerdas")
        self.geometry("1100x700")
        
        # Material You Dark Theme Colors
        self.colors = {
            'primary': '#6750A4',
            'primary_container': '#4F378B',
            'secondary': '#625B71',
            'secondary_container': '#4A4458',
            'surface': '#1C1B1F',
            'surface_variant': '#49454F',
            'surface_container': '#211F26',
            'surface_container_high': '#2B2930',
            'on_surface': '#E6E1E5',
            'on_surface_variant': '#CAC4D0',
            'outline': '#938F99',
            'outline_variant': '#49454F',
            'error': '#F2B8B5',
            'success': '#4CAF50',
            'warning': '#FF9800'
        }
        
        # Set custom color theme
        ctk.set_default_color_theme("blue")
        
        # Configure window
        self.configure(fg_color=self.colors['surface'])
        
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

    def sidebar(self):
        # Modern sidebar with Material You styling
        sidebar = ctk.CTkFrame(
            self, 
            width=280, 
            corner_radius=24,
            fg_color=self.colors['surface_container'],
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        sidebar.pack(side="left", fill="y", padx=16, pady=16)
        sidebar.pack_propagate(False)

        # App title with modern typography
        title_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        title_frame.pack(pady=(24, 32), padx=24, fill="x")
        
        title = ctk.CTkLabel(
            title_frame, 
            text="📚 Tutor Cerdas", 
            font=("Segoe UI", 28, "bold"),
            text_color=self.colors['on_surface']
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Find your perfect tutor",
            font=("Segoe UI", 14),
            text_color=self.colors['on_surface_variant']
        )
        subtitle.pack(pady=(4, 0))

        # Navigation buttons with Material You styling
        nav_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_frame.pack(fill="x", padx=16)
        
        register_btn = ctk.CTkButton(
            nav_frame, 
            text="➕ Daftarkan Tutor",
            font=("Segoe UI", 16, "bold"),
            height=56,
            corner_radius=28,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_container'],
            text_color="white",
            command=self.open_register_window
        )
        register_btn.pack(pady=(0, 12), fill="x")
        
        # User profile section
        profile_frame = ctk.CTkFrame(
            sidebar,
            corner_radius=16,
            fg_color=self.colors['surface_container_high'],
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        profile_frame.pack(side="bottom", fill="x", padx=16, pady=16)
        
        profile_label = ctk.CTkLabel(
            profile_frame,
            text=f"👤 {self.user_instance.username}",
            font=("Segoe UI", 16, "bold"),
            text_color=self.colors['on_surface']
        )
        profile_label.pack(pady=16)

    def main_area(self):
        # Main content container with modern styling
        self.content_container = ctk.CTkFrame(
            self, 
            corner_radius=24,
            fg_color=self.colors['surface_container'],
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        self.content_container.pack(expand=True, fill="both", padx=(0, 16), pady=16)
        
        # Modern search and filter section
        self.search_frame = ctk.CTkFrame(
            self.content_container, 
            corner_radius=20, 
            fg_color=self.colors['surface_container_high'],
            border_width=1,
            border_color=self.colors['outline_variant'],
            height=80
        )
        self.search_frame.pack(fill="x", padx=24, pady=24)
        self.search_frame.pack_propagate(False)
        
        # Configure grid for search frame
        self.search_frame.grid_columnconfigure(1, weight=1)
        
        # Search section
        search_label = ctk.CTkLabel(
            self.search_frame,
            text="🔍",
            font=("Segoe UI", 20),
            text_color=self.colors['on_surface_variant']
        )
        search_label.grid(row=0, column=0, padx=(20, 12), pady=20, sticky="w")
        
        # Modern search entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search tutors...",
            font=("Segoe UI", 16),
            height=40,
            corner_radius=20,
            border_width=0,
            fg_color=self.colors['surface_variant'],
            text_color=self.colors['on_surface'],
            placeholder_text_color=self.colors['on_surface_variant']
        )
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=(0, 16), pady=20)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Filter dropdown with modern styling
        self.filter_var = ctk.StringVar(value="All Subjects")
        dropdown_options = ["All Subjects"] + self.all_matkul
        
        self.filter_dropdown = ctk.CTkOptionMenu(
            self.search_frame,
            values=dropdown_options,
            variable=self.filter_var,   
            width=180,
            height=40,
            font=("Segoe UI", 14),
            dropdown_font=("Segoe UI", 14),
            fg_color=self.colors['secondary'],
            button_color=self.colors['secondary'],
            button_hover_color=self.colors['secondary_container'],
            dropdown_fg_color=self.colors['surface_container_high'],
            dropdown_text_color=self.colors['on_surface'],
            corner_radius=20,
            command=self.on_filter_change
        )
        self.filter_dropdown.grid(row=0, column=2, padx=(0, 20), pady=20)
        
        # Status section with modern typography
        status_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        status_frame.pack(fill="x", padx=24, pady=(0, 16))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="",
            font=("Segoe UI", 14),
            text_color=self.colors['on_surface_variant'],
            anchor="w"
        )
        self.status_label.pack(anchor="w")
        
        # Tutors display area with modern scrollable frame
        self.main_frame = ctk.CTkScrollableFrame(
            self.content_container, 
            corner_radius=20,
            fg_color=self.colors['surface'],
            scrollbar_button_color=self.colors['outline'],
            scrollbar_button_hover_color=self.colors['outline_variant']
        )
        self.main_frame.pack(expand=True, fill="both", padx=24, pady=(0, 24))

    def on_search_change(self, event=None):
        """Handle search as user types"""
        search_term = self.search_entry.get().strip().lower()
        if search_term:
            self.search_tutors()
        else:
            self.apply_current_filter()

    def on_filter_change(self, choice):
        """Handle filter dropdown change"""
        if choice == "All Subjects":
            self.current_filter = None
        else:
            self.current_filter = choice
        
        self.apply_current_filter()
    
    def apply_current_filter(self):
        """Apply the current filter and search term"""
        search_term = self.search_entry.get().strip().lower()
        
        if self.current_filter:
            filtered_tutors = self.user_instance.filterByMatkul(self.current_filter)
            self.current_tutors = filtered_tutors
            
            if search_term:
                filtered_tutors = [t for t in filtered_tutors if search_term in t.get("nama", "").lower()]
            
            self.display_tutors(filtered_tutors)
            
            if filtered_tutors:
                status_text = f"Showing {len(filtered_tutors)} tutors for '{self.current_filter}'"
            else:
                status_text = f"No tutors found for '{self.current_filter}'"
            
            self.show_status_message(status_text)
        else:
            all_tutors = self.user_instance.loadAllTutors()
            self.current_tutors = all_tutors
            
            if search_term:
                all_tutors = [t for t in all_tutors if search_term in t.get("nama", "").lower()]
            
            self.display_tutors(all_tutors)
            status_text = f"Showing all {len(all_tutors)} tutors"
            self.show_status_message(status_text)

    def search_tutors(self):
        """Search tutors by name"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            self.apply_current_filter()
            return
        
        filtered_tutors = []
        base_tutors = self.current_tutors if self.current_filter else self.user_instance.loadAllTutors()
        
        for tutor in base_tutors:
            if search_term in tutor.get("nama", "").lower():
                filtered_tutors.append(tutor)
        
        self.display_tutors(filtered_tutors)
        
        if filtered_tutors:
            status_text = f"Found {len(filtered_tutors)} tutors matching '{search_term}'"
        else:
            status_text = f"No tutors found matching '{search_term}'"
        
        self.show_status_message(status_text)

    def display_tutors(self, tutors):
        """Display the given list of tutors"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        if not tutors:
            no_results_frame = ctk.CTkFrame(
                self.main_frame,
                fg_color="transparent"
            )
            no_results_frame.pack(expand=True, fill="both")
            
            no_results_label = ctk.CTkLabel(
                no_results_frame,
                text="😔 No tutors found",
                font=("Segoe UI", 24, "bold"),
                text_color=self.colors['on_surface_variant']
            )
            no_results_label.pack(expand=True)
        else:
            for tutor in tutors:
                self.tutor_card(tutor)

    def show_status_message(self, message):
        self.status_label.configure(text=message)

    def refresh_tutors(self):
        self.filter_var.set("All Subjects")
        self.current_filter = None
        self.search_entry.delete(0, 'end')
        
        all_tutors = self.user_instance.loadAllTutors()
        self.current_tutors = all_tutors
        self.display_tutors(all_tutors)
        
        status_text = f"Showing all {len(all_tutors)} tutors"
        self.show_status_message(status_text)

    def open_register_window(self):
        RegisterTutor(self, self.user_instance)

    def open_chat(self, tutor_data):
        """Open chat window with specific tutor"""
        ChatWindow(self, tutor_data)

    def tutor_card(self, tutor):
        # Modern Material You card design
        card = ctk.CTkFrame(
            self.main_frame, 
            fg_color=self.colors['surface_container_high'],
            corner_radius=24,
            border_width=1,
            border_color=self.colors['outline_variant']
        )
        card.pack(pady=12, padx=20, fill="x")

        # Card content container
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="x", padx=24, pady=20)

        # Header with name and avatar
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 16))
        
        # Avatar circle
        avatar_frame = ctk.CTkFrame(
            header_frame,
            width=56,
            height=56,
            corner_radius=28,
            fg_color=self.colors['primary']
        )
        avatar_frame.pack(side="left")
        avatar_frame.pack_propagate(False)
        
        avatar_label = ctk.CTkLabel(
            avatar_frame,
            text="👨‍🏫",
            font=("Segoe UI", 24)
        )
        avatar_label.pack(expand=True)
        
        # Name and info
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True, padx=(16, 0))
        
        nama_label = ctk.CTkLabel(
            info_frame, 
            text=tutor['nama'], 
            font=("Segoe UI", 20, "bold"), 
            text_color=self.colors['on_surface'],
            anchor="w"
        )
        nama_label.pack(anchor="w")

        # Subjects with modern chips
        subjects_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        subjects_frame.pack(fill="x", pady=(0, 12))
        
        subjects_label = ctk.CTkLabel(
            subjects_frame,
            text="📚 Subjects:",
            font=("Segoe UI", 14, "bold"),
            text_color=self.colors['on_surface_variant']
        )
        subjects_label.pack(anchor="w", pady=(0, 8))
        
        # Subject chips container
        chips_frame = ctk.CTkFrame(subjects_frame, fg_color="transparent")
        chips_frame.pack(fill="x")
        
        for i, subject in enumerate(tutor['mata-kuliah'][:3]):  # Show max 3 subjects
            chip = ctk.CTkFrame(
                chips_frame,
                corner_radius=16,
                fg_color=self.colors['secondary_container'],
                height=32
            )
            chip.pack(side="left", padx=(0, 8))
            chip.pack_propagate(False)
            
            chip_label = ctk.CTkLabel(
                chip,
                text=subject,
                font=("Segoe UI", 12, "bold"),
                text_color=self.colors['on_surface']
            )
            chip_label.pack(padx=16, pady=8)

        # Details section
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(fill="x", pady=(0, 16))
        
        time_label = ctk.CTkLabel(
            details_frame, 
            text=f"⏰ {tutor['waktu-belajar']}", 
            font=("Segoe UI", 14), 
            text_color=self.colors['on_surface_variant']
        )
        time_label.pack(anchor="w", pady=2)
        
        location_label = ctk.CTkLabel(
            details_frame, 
            text=f"📍 {tutor['tempat-belajar']}", 
            font=("Segoe UI", 14), 
            text_color=self.colors['on_surface_variant']
        )
        location_label.pack(anchor="w", pady=2)

        # Action button
        action_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        action_frame.pack(fill="x")

        chat_button = ctk.CTkButton(
            action_frame, 
            text="💬 Start Chat",
            font=("Segoe UI", 16, "bold"),
            height=48,
            corner_radius=24,
            fg_color=self.colors['primary'],
            hover_color=self.colors['primary_container'],
            text_color="white",
            command=lambda: self.open_chat(tutor)
        )
        chat_button.pack(side="right")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    gui = GUI(User())
    gui.run()