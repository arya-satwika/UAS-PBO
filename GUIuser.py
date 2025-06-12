import customtkinter as ctk
from tkinter import messagebox
from theme import color_pallete
from user import User

# Set consistent appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class UserProfile(ctk.CTkToplevel):
    def __init__(self, master, user):
        super().__init__(master)
        
        # Configure window
        self.title("User Profile - TutorCerdas")
        self.geometry("800x450")
        self.resizable(True, True)
        self.configure(fg_color=color_pallete["background"])
        self.grab_set()
        self.focus_set()
        self.center_window()
        # Sample user data - in real app, this would come from a database
        self.user_data = user
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
        # Main container
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header
        self.create_header()
        
        # Tabview
        self.create_tabview()
    
    def create_header(self):
        # Header frame
        header_frame = ctk.CTkFrame(
            self, 
            height=100, 
            corner_radius=25,
            fg_color=color_pallete["sidebar_fill"],
            border_color=color_pallete["sidebar_border"],
            border_width=1
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Profile picture placeholder
        profile_frame = ctk.CTkFrame(
            header_frame, 
            width=80, 
            height=80, 
            corner_radius=40,
            fg_color=color_pallete["clickable_bg"]
        )
        profile_frame.grid(row=0, column=0, padx=20, pady=10)
        
        profile_label = ctk.CTkLabel(
            profile_frame, 
            text=self.user_data.username[:2].upper(),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        profile_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # User info
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame,
            text=self.user_data.username,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"{self.user_data.prodi} • Angkatan {self.user_data.angkatan}",
            font=ctk.CTkFont(size=14),
            text_color=color_pallete["text_secondary"]
        )
        details_label.grid(row=1, column=0, sticky="w")
    
    def create_tabview(self):
        # Create tabview
        self.tabview = ctk.CTkTabview(
            self, 
            width=750, 
            height=300,
            fg_color=color_pallete["main_bg"],
            segmented_button_fg_color=color_pallete["clickable_bg"],
            segmented_button_selected_color=color_pallete["clickable_border"],
            segmented_button_unselected_color=color_pallete["clickable_bg"],
            segmented_button_unselected_hover_color=color_pallete["sidebar_border"],
            segmented_button_selected_hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color=color_pallete["main_border"],
            border_width=1,
            corner_radius=25,
        )
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Add tabs
        self.tabview.add("Nama")
        self.tabview.add("Saldo")
        
        # Configure tab content
        self.setup_nama_tab()
        self.setup_saldo_tab()
    
    def setup_nama_tab(self):
        tab = self.tabview.tab("Nama")
        
        # Main info frame
        info_frame = ctk.CTkFrame(
            tab,
            fg_color=color_pallete["card_bg"],
            border_color=color_pallete["card_border"],
            border_width=1,
            corner_radius=20
        )
        info_frame.pack(fill="x", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            info_frame,
            text="Informasi Profil",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        title_label.pack(pady=(20, 10))
        
        # Create info grid
        grid_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        grid_frame.pack(fill="x", expand=True, padx=20, pady=10)
        
        # Configure grid
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Program Studi
        self.create_info_item(grid_frame, "Program Studi", self.user_data.prodi, 0, 0)

        # Angkatan
        self.create_info_item(grid_frame, "Angkatan", self.user_data.angkatan, 0, 1)

        # Edit button
        edit_btn = ctk.CTkButton(
            info_frame,
            text="Edit Profil",
            command=self.edit_profile,
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            corner_radius=20
        )
        edit_btn.pack(pady=20)
    
    def create_info_item(self, parent, label_text, value_text, row, col):
        item_frame = ctk.CTkFrame(
            parent,
            fg_color=color_pallete["highlight_bg"],
            border_color=color_pallete["highlight_border"],
            border_width=1,
            corner_radius=20
        )
        item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        label = ctk.CTkLabel(
            item_frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color_pallete["text_secondary"]
        )
        label.pack(pady=(10, 5))
        
        value = ctk.CTkLabel(
            item_frame,
            text=str(value_text),
            font=ctk.CTkFont(size=14),
            text_color=color_pallete["text_primary"]
        )
        value.pack(pady=(0, 10))
    
    def setup_saldo_tab(self):
        tab = self.tabview.tab("Saldo")
        
        # Saldo frame
        saldo_frame = ctk.CTkFrame(
            tab,
            fg_color=color_pallete["card_bg"],
            border_color=color_pallete["card_border"],
            border_width=1,
            corner_radius=20
        )
        saldo_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        saldo_title = ctk.CTkLabel(
            saldo_frame,
            text="Saldo Saat Ini",
            font=ctk.CTkFont(size=14, family="Helvetica"),
            text_color=color_pallete["text_secondary"],
            corner_radius=30
        )
        saldo_title.pack(pady=(20, 5))
        
        saldo_amount = ctk.CTkLabel(
            saldo_frame,
            text=f"Rp {self.user_data.saldo:,}",
            font=ctk.CTkFont(size=30, family="Helvetica", weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        saldo_amount.pack(pady=(0, 20))
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(saldo_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        topup_btn = ctk.CTkButton(
            btn_frame,
            text="Top Up Saldo",
            command=self.topup_saldo,
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color=color_pallete["clickable_border"],
            border_width=1,
            corner_radius=20
        )
        topup_btn.pack(side="left", padx=(0, 10))
        
        

    def edit_profile(self):
        messagebox.showinfo("Edit Profil", "Fitur edit profil akan segera tersedia!")
    
    def topup_saldo(self):
        # Create top-up window
        topup_window = ctk.CTkToplevel(self)
        topup_window.grab_set()
        topup_window.focus_set()
        topup_window.title("Top Up Saldo")
        topup_window.geometry("400x300")
        topup_window.transient(self)
        topup_window.configure(fg_color=color_pallete["background"])
        
        # Center the window
        topup_window.after(100, lambda: topup_window.lift())
        
        title_label = ctk.CTkLabel(
            topup_window,
            text="Top Up Saldo",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=color_pallete["text_primary"]
        )
        title_label.pack(pady=20)
        
        amount_label = ctk.CTkLabel(
            topup_window, 
            text="Masukkan jumlah:",
            text_color=color_pallete["text_secondary"]
        )
        amount_label.pack(pady=10)
        
        amount_entry = ctk.CTkEntry(
            topup_window,
            placeholder_text="Contoh: 50000",
            width=200,
            fg_color=color_pallete["entry_bg"],
            border_color=color_pallete["entry_border"],
            text_color=color_pallete["entry_text"],
            corner_radius=20
        )
        amount_entry.pack(pady=10)
        
        topup_btn = ctk.CTkButton(
            topup_window,
            text="Top Up",
            command=lambda: self._handle_topup(amount_entry, topup_window),
            fg_color=color_pallete["clickable_bg"],
            hover_color=color_pallete["clickable_border"],
            text_color=color_pallete["text_clickable"],
            border_color= color_pallete["clickable_border"],
            border_width=1,
            corner_radius=20
        )
        topup_btn.pack(pady=20)

    def _handle_topup(self, amount_entry, topup_window):
        try:
            amount = int(amount_entry.get())
            if amount > 0:
                self.user_data.topup_saldo(amount)
                messagebox.showinfo("Sukses", "Top up succesfull")
                topup_window.destroy()
                # Refresh saldo tab (recreate tabview or saldo label)
                self.tabview.destroy()
                self.create_tabview()
            else:
                messagebox.showerror("Error", "Masukkan jumlah yang valid.")
        except Exception as e:
            messagebox.showerror("Error", f"Masukkan jumlah yang valid.\n{e}")
