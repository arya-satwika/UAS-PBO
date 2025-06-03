import customtkinter as ctk
# from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class TestApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("pepek Clone")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sample data
        self.categories = [
            "Moving", "Cleaning", "Handyman", "Delivery", "Furniture Assembly",
            "Mounting", "Yard Work", "Personal Assistant", "Painting", "Plumbing"
        ]
        
        self.tasks = [
            {
                "title": "Help with apartment move",
                "category": "Moving",
                "price": "$150",
                "location": "Manhattan, NY",
                "description": "Need help moving from a 2-bedroom apartment to a new place. Heavy furniture included.",
                "date": "Today",
                "rating": 4.8,
                "reviews": 127
            },
            {
                "title": "Deep clean 3-bedroom house",
                "category": "Cleaning",
                "price": "$200",
                "location": "Brooklyn, NY",
                "description": "Post-renovation deep cleaning needed. All supplies provided.",
                "date": "Tomorrow",
                "rating": 4.9,
                "reviews": 89
            },
            {
                "title": "Mount TV on wall",
                "category": "Mounting",
                "price": "$75",
                "location": "Queens, NY",
                "description": "Mount 55-inch TV on living room wall. All hardware provided.",
                "date": "This weekend",
                "rating": 4.7,
                "reviews": 203
            },
            {
                "title": "Assemble IKEA furniture",
                "category": "Furniture Assembly",
                "price": "$120",
                "location": "Manhattan, NY",
                "description": "Need help assembling bedroom set from IKEA. 4-5 pieces total.",
                "date": "Next week",
                "rating": 4.6,
                "reviews": 156
            },
            {
                "title": "Grocery delivery and setup",
                "category": "Personal Assistant",
                "price": "$45",
                "location": "Bronx, NY",
                "description": "Weekly grocery shopping and kitchen organization.",
                "date": "Today",
                "rating": 4.8,
                "reviews": 92
            }
        ]
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
    def create_sidebar(self):
        # Sidebar frame
        self.sidebar_frame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="pepek", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = ["Browse Tasks", "My Tasks", "Messages", "Profile", "Settings"]
        
        for i, item in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=item,
                width=200,
                height=40,
                command=lambda x=item: self.navigate_to(x)
            )
            btn.grid(row=i+1, column=0, padx=20, pady=5)
            self.nav_buttons.append(btn)
        
        # Categories section
        self.categories_label = ctk.CTkLabel(
            self.sidebar_frame,
            text="Categories",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.categories_label.grid(row=6, column=0, padx=20, pady=(20, 10))
        
        # Categories scrollable frame
        self.categories_frame = ctk.CTkScrollableFrame(
            self.sidebar_frame,
            width=200,
            height=200
        )
        self.categories_frame.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        
        for category in self.categories:
            cat_btn = ctk.CTkButton(
                self.categories_frame,
                text=category,
                width=180,
                height=30,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray20"),
                command=lambda x=category: self.filter_by_category(x)
            )
            cat_btn.pack(pady=2, padx=5, fill="x")
    
    def create_main_content(self):
        # Main content frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)
        
        # Header
        self.create_header()
        
        # Search and filters
        self.create_search_section()
        
        # Tasks grid
        self.create_tasks_section()
    
    def create_header(self):
        # Header frame
        self.header_frame = ctk.CTkFrame(self.main_frame, height=80)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        # Welcome message
        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text="Find the perfect task for you",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # User info
        self.user_frame = ctk.CTkFrame(self.header_frame)
        self.user_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text="John Doe",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.user_label.pack(side="left", padx=10, pady=10)
        
        self.balance_label = ctk.CTkLabel(
            self.user_frame,
            text="Balance: $250",
            font=ctk.CTkFont(size=12)
        )
        self.balance_label.pack(side="left", padx=(0, 10), pady=10)
    
    def create_search_section(self):
        # Search frame
        self.search_frame = ctk.CTkFrame(self.main_frame, height=60)
        self.search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.search_frame.grid_columnconfigure(0, weight=1)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Search tasks...",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        
        # Search button
        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=100,
            height=40,
            command=self.search_tasks
        )
        self.search_btn.grid(row=0, column=1, padx=(5, 20), pady=10)
        
        # Filter buttons
        self.filter_frame = ctk.CTkFrame(self.search_frame)
        self.filter_frame.grid(row=0, column=2, padx=(0, 20), pady=10)
        
        filters = ["All", "Today", "This Week", "High Rated"]
        for i, filter_name in enumerate(filters):
            filter_btn = ctk.CTkButton(
                self.filter_frame,
                text=filter_name,
                width=80,
                height=30,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray20"),
                command=lambda x=filter_name: self.apply_filter(x)
            )
            filter_btn.pack(side="left", padx=2, pady=5)
    
    def create_tasks_section(self):
        # Tasks scrollable frame
        self.tasks_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.tasks_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.tasks_frame.grid_columnconfigure(0, weight=1)
        
        # Display tasks
        self.display_tasks()
    
    def display_tasks(self):
        # Clear existing tasks
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Create task cards
        for i, task in enumerate(self.tasks):
            self.create_task_card(task, i)
    
    def create_task_card(self, task, index):
        # Task card frame
        card_frame = ctk.CTkFrame(self.tasks_frame, height=150)
        card_frame.grid(row=index, column=0, sticky="ew", padx=10, pady=5)
        card_frame.grid_columnconfigure(1, weight=1)
        
        # Task image placeholder
        image_frame = ctk.CTkFrame(card_frame, width=120, height=120)
        image_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nw")
        
        image_label = ctk.CTkLabel(
            image_frame,
            text="📋",
            font=ctk.CTkFont(size=40)
        )
        image_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Task details frame
        details_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        details_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=15)
        details_frame.grid_columnconfigure(0, weight=1)
        
        # Title and category
        title_label = ctk.CTkLabel(
            details_frame,
            text=task["title"],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        
        category_label = ctk.CTkLabel(
            details_frame,
            text=f"Category: {task['category']}",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        category_label.grid(row=1, column=0, sticky="ew")
        
        # Description
        desc_label = ctk.CTkLabel(
            details_frame,
            text=task["description"],
            font=ctk.CTkFont(size=12),
            anchor="w",
            wraplength=400
        )
        desc_label.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Location and date
        location_label = ctk.CTkLabel(
            details_frame,
            text=f"📍 {task['location']} • 📅 {task['date']}",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        location_label.grid(row=3, column=0, sticky="ew")
        
        # Rating
        rating_label = ctk.CTkLabel(
            details_frame,
            text=f"⭐ {task['rating']} ({task['reviews']} reviews)",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        rating_label.grid(row=4, column=0, sticky="ew")
        
        # Price and action frame
        action_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        action_frame.grid(row=0, column=2, padx=15, pady=15, sticky="ne")
        
        # Price
        price_label = ctk.CTkLabel(
            action_frame,
            text=task["price"],
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="green"
        )
        price_label.pack(pady=(0, 10))
        
        # Apply button
        apply_btn = ctk.CTkButton(
            action_frame,
            text="Apply Now",
            width=100,
            height=35,
            command=lambda t=task: self.apply_for_task(t)
        )
        apply_btn.pack()
        
        # View details button
        details_btn = ctk.CTkButton(
            action_frame,
            text="View Details",
            width=100,
            height=30,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray20"),
            command=lambda t=task: self.view_task_details(t)
        )
        details_btn.pack(pady=(5, 0))
    
    def navigate_to(self, section):
        print(f"Navigating to: {section}")
        # Here you would implement navigation logic
        
    def filter_by_category(self, category):
        print(f"Filtering by category: {category}")
        # Here you would implement category filtering
        
    def search_tasks(self):
        search_term = self.search_entry.get()
        print(f"Searching for: {search_term}")
        # Here you would implement search functionality
        
    def apply_filter(self, filter_name):
        print(f"Applying filter: {filter_name}")
        # Here you would implement filter logic
        
    def apply_for_task(self, task):
        print(f"Applying for task: {task['title']}")
        # Here you would implement task application logic
        
    def view_task_details(self, task):
        print(f"Viewing details for: {task['title']}")
        # Here you would implement task details view
        
    def run(self):
        self.root.mainloop()

# Create and run the application
if __name__ == "__main__":
    app = TestApp()
    app.run()