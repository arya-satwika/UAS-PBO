import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import hashlib
import datetime
import json

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class AuthenticationSystem:
    def __init__(self):
        # Dummy user database
        self.users_db = {
            "john.doe@email.com": {
                "password": self.hash_password("password123"),
                "name": "John Doe",
                "phone": "+1-555-0123",
                "address": "123 Main St, New York, NY",
                "balance": 250.00,
                "rating": 4.8,
                "tasks_completed": 47,
                "member_since": "2023-01-15",
                "profile_type": "tasker"  # or "client"
            },
            "jane.smith@email.com": {
                "password": self.hash_password("mypassword"),
                "name": "Jane Smith",
                "phone": "+1-555-0456",
                "address": "456 Oak Ave, Brooklyn, NY",
                "balance": 180.50,
                "rating": 4.9,
                "tasks_completed": 23,
                "member_since": "2023-03-20",
                "profile_type": "client"
            },
            "mike.wilson@email.com": {
                "password": self.hash_password("secure123"),
                "name": "Mike Wilson",
                "phone": "+1-555-0789",
                "address": "789 Pine St, Queens, NY",
                "balance": 320.75,
                "rating": 4.7,
                "tasks_completed": 89,
                "member_since": "2022-11-08",
                "profile_type": "tasker"
            }
        }
        
        self.current_user = None
        
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self, email, password):
        """Authenticate user with email and password"""
        if email in self.users_db:
            stored_password = self.users_db[email]["password"]
            if stored_password == self.hash_password(password):
                self.current_user = {
                    "email": email,
                    **self.users_db[email]
                }
                return True
        return False
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self):
        """Get current logged-in user"""
        return self.current_user

class LoginWindow:
    def __init__(self, auth_system, on_login_success):
        self.auth_system = auth_system
        self.on_login_success = on_login_success
        
        # Create login window
        self.window = ctk.CTk()
        self.window.title("TaskRabbit - Login")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Configure grid
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        # Current mode (login or register)
        self.current_mode = "login"
        
        self.setup_ui()
        
    def center_window(self):
        """Center the window on screen"""
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"800x600+{x}+{y}")
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
        
        # Left side - Welcome/Info
        self.create_welcome_section()
        
        # Right side - Login form
        self.create_form_section()
        
    def create_header(self):
        """Create header with logo and title"""
        header_frame = ctk.CTkFrame(self.main_frame, height=80, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))
        
        # Logo and title
        logo_label = ctk.CTkLabel(
            header_frame,
            text="🐰 TaskRabbit",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=("#1f538d", "#4a9eff")
        )
        logo_label.pack(pady=20)
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Connect with skilled Taskers in your neighborhood",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack()
    
    def create_welcome_section(self):
        """Create welcome section with info"""
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Welcome content
        welcome_title = ctk.CTkLabel(
            welcome_frame,
            text="Welcome Back!",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        welcome_title.pack(pady=(40, 20))
        
        # Features list
        features = [
            "🏠 Home services at your fingertips",
            "⭐ Trusted and rated Taskers",
            "💰 Transparent pricing",
            "🔒 Secure payments",
            "📱 Easy booking process"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(
                welcome_frame,
                text=feature,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            feature_label.pack(pady=8, padx=30, fill="x")
        
        # Demo credentials info
        demo_frame = ctk.CTkFrame(welcome_frame)
        demo_frame.pack(pady=30, padx=20, fill="x")
        
        demo_title = ctk.CTkLabel(
            demo_frame,
            text="Demo Credentials",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        demo_title.pack(pady=(15, 10))
        
        demo_info = [
            "Email: john.doe@email.com",
            "Password: password123",
            "",
            "Email: jane.smith@email.com", 
            "Password: mypassword"
        ]
        
        for info in demo_info:
            if info:
                info_label = ctk.CTkLabel(
                    demo_frame,
                    text=info,
                    font=ctk.CTkFont(size=12),
                    text_color="gray"
                )
                info_label.pack(pady=2)
            else:
                ctk.CTkLabel(demo_frame, text="").pack(pady=5)
        
        demo_frame.pack_configure(pady=(30, 15))
    
    def create_form_section(self):
        """Create login form section"""
        self.form_frame = ctk.CTkFrame(self.content_frame)
        self.form_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        # Form title
        self.form_title = ctk.CTkLabel(
            self.form_frame,
            text="Sign In",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.form_title.pack(pady=(40, 30))
        
        # Form fields container
        self.fields_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.fields_frame.pack(fill="both", expand=True, padx=30)
        
        # Only create login form, no register form
        self.create_login_form()
        
    def create_login_form(self):
        """Create login form fields"""
        # Clear existing fields
        for widget in self.fields_frame.winfo_children():
            widget.destroy()
        
        # Email field
        email_label = ctk.CTkLabel(self.fields_frame, text="Email Address", anchor="w")
        email_label.pack(fill="x", pady=(0, 5))
        
        self.email_entry = ctk.CTkEntry(
            self.fields_frame,
            placeholder_text="Enter your email",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        # Password field
        password_label = ctk.CTkLabel(self.fields_frame, text="Password", anchor="w")
        password_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            self.fields_frame,
            placeholder_text="Enter your password",
            show="*",
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(fill="x", pady=(0, 20))
        
        # Login button
        self.login_btn = ctk.CTkButton(
            self.fields_frame,
            text="Sign In",
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.handle_login
        )
        self.login_btn.pack(fill="x", pady=(0, 15))
        
        # Forgot password link
        forgot_btn = ctk.CTkButton(
            self.fields_frame,
            text="Forgot Password?",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray20"),
            height=30,
            command=self.forgot_password
        )
        forgot_btn.pack(pady=(0, 20))
        
        # Divider
        divider_frame = ctk.CTkFrame(self.fields_frame, height=2)
        divider_frame.pack(fill="x", pady=15)
        
        # No register switch or register form
        # Bind Enter key to login
        self.window.bind('<Return>', lambda event: self.handle_login())
    
    def handle_login(self):
        """Handle login attempt"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.auth_system.authenticate_user(email, password):
            messagebox.showinfo("Success", f"Welcome back, {self.auth_system.get_current_user()['name']}!")
            self.window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid email or password")
            self.password_entry.delete(0, 'end')
    
    def forgot_password(self):
        """Handle forgot password"""
        messagebox.showinfo("Forgot Password", "Password reset functionality would be implemented here.\n\nFor demo purposes, use the provided credentials.")
    
    def run(self):
        """Run the login window"""
        self.window.mainloop()

# Updated TaskRabbit main app with authentication
class TaskRabbitApp:
    def __init__(self, auth_system):
        self.auth_system = auth_system
        self.root = ctk.CTk()
        self.root.title("TaskRabbit Clone")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure grid weights
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sample data (same as before)
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
            text="TaskRabbit", 
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
        
        # Logout button
        self.logout_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="Logout",
            width=200,
            height=40,
            fg_color="red",
            hover_color="darkred",
            command=self.logout
        )
        self.logout_btn.grid(row=8, column=0, padx=20, pady=(20, 20))
    
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
        user = self.auth_system.get_current_user()
        welcome_text = f"Welcome back, {user['name']}!"
        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text=welcome_text,
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.welcome_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # User info
        self.user_frame = ctk.CTkFrame(self.header_frame)
        self.user_frame.grid(row=0, column=2, padx=20, pady=10, sticky="e")
        
        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text=user['name'],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.user_label.pack(side="left", padx=10, pady=10)
        
        self.balance_label = ctk.CTkLabel(
            self.user_frame,
            text=f"Balance: ${user['balance']:.2f}",
            font=ctk.CTkFont(size=12)
        )
        self.balance_label.pack(side="left", padx=(0, 10), pady=10)
        
        # User rating
        self.rating_label = ctk.CTkLabel(
            self.user_frame,
            text=f"⭐ {user['rating']} ({user['tasks_completed']} tasks)",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.rating_label.pack(side="left", padx=(0, 10), pady=10)
    
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
        if section == "Profile":
            self.show_profile()
        # Here you would implement other navigation logic
        
    def show_profile(self):
        """Show user profile information"""
        user = self.auth_system.get_current_user()
        profile_info = f"""
Profile Information:
Name: {user['name']}
Email: {user['email']}
Phone: {user['phone']}
Address: {user['address']}
Profile Type: {user['profile_type'].title()}
Balance: ${user['balance']:.2f}
Rating: {user['rating']} ⭐
Tasks Completed: {user['tasks_completed']}
Member Since: {user['member_since']}
        """
        messagebox.showinfo("Profile", profile_info)
        
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
        user = self.auth_system.get_current_user()
        messagebox.showinfo("Task Application", f"Applied for task: {task['title']}\n\nYour application has been submitted!")
        
    def view_task_details(self, task):
        details = f"""
Task Details:
Title: {task['title']}
Category: {task['category']}
Price: {task['price']}
Location: {task['location']}
Date: {task['date']}
Rating: {task['rating']} ⭐ ({task['reviews']} reviews)

Description:
{task['description']}
        """
        messagebox.showinfo("Task Details", details)
    
    def logout(self):
        """Logout and return to login screen"""
        self.auth_system.logout()
        self.root.destroy()
        main()
        
    def run(self):
        self.root.mainloop()

def main():
    """Main application entry point"""
    # Create authentication system
    auth_system = AuthenticationSystem()
    
    def on_login_success():
        """Callback when login is successful"""
        # Create and run main app
        app = TaskRabbitApp(auth_system)
        app.run()
    
    # Create and show login window
    login_window = LoginWindow(auth_system, on_login_success)
    login_window.run()

# Run the application
if __name__ == "__main__":
    main()