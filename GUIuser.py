import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class UserProfile(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("User Profile - TutorCerdas")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Sample user data - in real app, this would come from a database
        self.user_data = {
            "nama": "Ahmad Rizky Pratama",
            "saldo": 250000,
            "angkatan": "2021",
            "prodi": "Teknik Informatika",
            "email": "ahmad.rizky@university.ac.id",
            "fakultas": "Fakultas Ilmu Komputer",
            "semester": 5,
            "sks_ditempuh": 90,
            "ipk": 3.75,
            "dosen_pa": "Dr. Budi Santoso, M.Kom.",
            "mata_kuliah": [
                {"nama": "Pemrograman Web Lanjut", "sks": 3},
                {"nama": "Kecerdasan Buatan", "sks": 4},
                {"nama": "Analisis Algoritma", "sks": 3},
                {"nama": "Basis Data Lanjut", "sks": 3}
            ],
            "riwayat_transaksi": [
                {"deskripsi": "Pembayaran Tutor Matematika", "jumlah": -50000, "tanggal": "2023-06-10"},
                {"deskripsi": "Top Up Saldo", "jumlah": 100000, "tanggal": "2023-06-08"},
                {"deskripsi": "Pembayaran Tutor Fisika", "jumlah": -45000, "tanggal": "2023-06-05"},
                {"deskripsi": "Pembayaran Tutor Kimia", "jumlah": -40000, "tanggal": "2023-06-03"}
            ]
        }
        
        self.setup_ui()
    
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
        header_frame = ctk.CTkFrame(self, height=100, corner_radius=10)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Profile picture placeholder
        profile_frame = ctk.CTkFrame(header_frame, width=80, height=80, corner_radius=40)
        profile_frame.grid(row=0, column=0, padx=20, pady=10)
        
        profile_label = ctk.CTkLabel(
            profile_frame, 
            text=self.user_data["nama"][:2].upper(),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        profile_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # User info
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="w", padx=20, pady=10)
        
        name_label = ctk.CTkLabel(
            info_frame, 
            text=self.user_data["nama"],
            font=ctk.CTkFont(size=20, weight="bold")
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        details_label = ctk.CTkLabel(
            info_frame,
            text=f"{self.user_data['prodi']} • Angkatan {self.user_data['angkatan']}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        details_label.grid(row=1, column=0, sticky="w")
    
    def create_tabview(self):
        # Create tabview
        self.tabview = ctk.CTkTabview(self, width=750, height=450)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Add tabs
        self.tabview.add("Nama")
        self.tabview.add("Saldo")
        self.tabview.add("Angkatan")
        self.tabview.add("Prodi")
        
        # Configure tab content
        self.setup_nama_tab()
        self.setup_saldo_tab()
        self.setup_angkatan_tab()
        self.setup_prodi_tab()
    
    def setup_nama_tab(self):
        tab = self.tabview.tab("Nama")
        
        # Main info frame
        info_frame = ctk.CTkFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            info_frame,
            text="Informasi Profil",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Create info grid
        grid_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configure grid
        grid_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Name
        self.create_info_item(grid_frame, "Nama Lengkap", self.user_data["nama"], 0, 0)
        
        # Email
        self.create_info_item(grid_frame, "Email", self.user_data["email"], 0, 1)
        
        # Program Studi
        self.create_info_item(grid_frame, "Program Studi", self.user_data["prodi"], 1, 0)
        
        # Angkatan
        self.create_info_item(grid_frame, "Angkatan", self.user_data["angkatan"], 1, 1)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            info_frame,
            text="Edit Profil",
            command=self.edit_profile
        )
        edit_btn.pack(pady=20)
    
    def create_info_item(self, parent, label_text, value_text, row, col):
        item_frame = ctk.CTkFrame(parent)
        item_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        label = ctk.CTkLabel(
            item_frame,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        label.pack(pady=(10, 5))
        
        value = ctk.CTkLabel(
            item_frame,
            text=str(value_text),
            font=ctk.CTkFont(size=14)
        )
        value.pack(pady=(0, 10))
    
    def setup_saldo_tab(self):
        tab = self.tabview.tab("Saldo")
        
        # Saldo frame
        saldo_frame = ctk.CTkFrame(tab)
        saldo_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        saldo_title = ctk.CTkLabel(
            saldo_frame,
            text="Saldo Saat Ini",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="gray"
        )
        saldo_title.pack(pady=(20, 5))
        
        saldo_amount = ctk.CTkLabel(
            saldo_frame,
            text=f"Rp {self.user_data['saldo']:,}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        saldo_amount.pack(pady=(0, 20))
        
        # Buttons frame
        btn_frame = ctk.CTkFrame(saldo_frame, fg_color="transparent")
        btn_frame.pack(pady=(0, 20))
        
        topup_btn = ctk.CTkButton(
            btn_frame,
            text="Top Up Saldo",
            command=self.topup_saldo
        )
        topup_btn.pack(side="left", padx=(0, 10))
        
        history_btn = ctk.CTkButton(
            btn_frame,
            text="Lihat Semua Transaksi",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.show_all_transactions
        )
        history_btn.pack(side="left")
        
        # Transaction history
        history_frame = ctk.CTkFrame(tab)
        history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        history_title = ctk.CTkLabel(
            history_frame,
            text="Riwayat Transaksi Terbaru",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        history_title.pack(pady=(20, 10))
        
        # Scrollable frame for transactions
        scrollable_frame = ctk.CTkScrollableFrame(history_frame, height=200)
        scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for transaction in self.user_data["riwayat_transaksi"]:
            self.create_transaction_item(scrollable_frame, transaction)
    
    def create_transaction_item(self, parent, transaction):
        item_frame = ctk.CTkFrame(parent)
        item_frame.pack(fill="x", pady=5)
        
        # Configure grid
        item_frame.grid_columnconfigure(0, weight=1)
        
        desc_label = ctk.CTkLabel(
            item_frame,
            text=transaction["deskripsi"],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        desc_label.grid(row=0, column=0, sticky="w", padx=15, pady=(10, 0))
        
        date_label = ctk.CTkLabel(
            item_frame,
            text=transaction["tanggal"],
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="w"
        )
        date_label.grid(row=1, column=0, sticky="w", padx=15, pady=(0, 10))
        
        amount_color = "green" if transaction["jumlah"] > 0 else "red"
        amount_text = f"+Rp {transaction['jumlah']:,}" if transaction["jumlah"] > 0 else f"Rp {transaction['jumlah']:,}"
        
        amount_label = ctk.CTkLabel(
            item_frame,
            text=amount_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=amount_color
        )
        amount_label.grid(row=0, column=1, rowspan=2, padx=15, pady=10)
    
    def setup_angkatan_tab(self):
        tab = self.tabview.tab("Angkatan")
        
        # Main frame
        main_frame = ctk.CTkFrame(tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="Informasi Angkatan",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        # Angkatan info
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20)
        info_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.create_info_item(info_frame, "Tahun Angkatan", self.user_data["angkatan"], 0, 0)
        self.create_info_item(info_frame, "Status", "Aktif", 0, 1)
        
        # Academic info
        academic_frame = ctk.CTkFrame(main_frame)
        academic_frame.pack(fill="x", padx=20, pady=20)
        
        academic_title = ctk.CTkLabel(
            academic_frame,
            text="Informasi Akademik",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        academic_title.pack(pady=(15, 10))
        
        # Academic details
        details = [
            ("Semester", str(self.user_data["semester"])),
            ("SKS Ditempuh", str(self.user_data["sks_ditempuh"])),
            ("IPK", str(self.user_data["ipk"]))
        ]
        
        for label, value in details:
            detail_frame = ctk.CTkFrame(academic_frame, fg_color="transparent")
            detail_frame.pack(fill="x", padx=15, pady=2)
            
            detail_label = ctk.CTkLabel(
                detail_frame,
                text=label,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            detail_label.pack(side="left")
            
            detail_value = ctk.CTkLabel(
                detail_frame,
                text=value,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="e"
            )
            detail_value.pack(side="right")
        
        # Button
        detail_btn = ctk.CTkButton(
            main_frame,
            text="Lihat Detail Akademik",
            command=self.show_academic_details
        )
        detail_btn.pack(pady=20)
    
    def setup_prodi_tab(self):
        tab = self.tabview.tab("Prodi")
        
        # Main frame
        main_frame = ctk.CTkFrame(tab)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="Program Studi",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        # Program info
        info_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20)
        info_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.create_info_item(info_frame, "Program Studi", self.user_data["prodi"], 0, 0)
        self.create_info_item(info_frame, "Fakultas", self.user_data["fakultas"], 0, 1)
        
        # Dosen PA
        dosen_frame = ctk.CTkFrame(main_frame)
        dosen_frame.pack(fill="x", padx=20, pady=20)
        
        dosen_title = ctk.CTkLabel(
            dosen_frame,
            text="Dosen Pembimbing Akademik",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        dosen_title.pack(pady=(15, 10))
        
        dosen_name = ctk.CTkLabel(
            dosen_frame,
            text=self.user_data["dosen_pa"],
            font=ctk.CTkFont(size=14)
        )
        dosen_name.pack(pady=(0, 15))
        
        # Mata kuliah
        matkul_frame = ctk.CTkFrame(main_frame)
        matkul_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        matkul_title = ctk.CTkLabel(
            matkul_frame,
            text="Mata Kuliah Semester Ini",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        matkul_title.pack(pady=(15, 10))
        
        # Scrollable frame for courses
        courses_frame = ctk.CTkScrollableFrame(matkul_frame, height=150)
        courses_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        for course in self.user_data["mata_kuliah"]:
            course_frame = ctk.CTkFrame(courses_frame, fg_color="transparent")
            course_frame.pack(fill="x", pady=2)
            
            course_name = ctk.CTkLabel(
                course_frame,
                text=course["nama"],
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            course_name.pack(side="left")
            
            course_sks = ctk.CTkLabel(
                course_frame,
                text=f"{course['sks']} SKS",
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="e"
            )
            course_sks.pack(side="right")
        
        # Button
        curriculum_btn = ctk.CTkButton(
            main_frame,
            text="Lihat Kurikulum Lengkap",
            command=self.show_curriculum
        )
        curriculum_btn.pack(pady=(0, 20))
    
    # Event handlers
    def edit_profile(self):
        messagebox.showinfo("Edit Profil", "Fitur edit profil akan segera tersedia!")
    
    def topup_saldo(self):
        # Create top-up window
        topup_window = ctk.CTkToplevel(self)
        topup_window.title("Top Up Saldo")
        topup_window.geometry("400x300")
        topup_window.transient(self)
        topup_window.grab_set()
        
        # Center the window
        topup_window.after(100, lambda: topup_window.lift())
        
        title_label = ctk.CTkLabel(
            topup_window,
            text="Top Up Saldo",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)
        
        amount_label = ctk.CTkLabel(topup_window, text="Masukkan jumlah:")
        amount_label.pack(pady=10)
        
        amount_entry = ctk.CTkEntry(
            topup_window,
            placeholder_text="Contoh: 50000",
            width=200
        )
        amount_entry.pack(pady=10)
        
        def process_topup():
            try:
                amount = int(amount_entry.get())
                if amount > 0:
                    self.user_data["saldo"] += amount
                    self.user_data["riwayat_transaksi"].insert(0, {
                        "deskripsi": "Top Up Saldo",
                        "jumlah": amount,
                        "tanggal": "2023-06-12"
                    })
                    messagebox.showinfo("Berhasil", f"Saldo berhasil ditambah Rp {amount:,}")
                    topup_window.destroy()
                    # Refresh the saldo tab
                    self.setup_saldo_tab()
                else:
                    messagebox.showerror("Error", "Jumlah harus lebih dari 0")
            except ValueError:
                messagebox.showerror("Error", "Masukkan jumlah yang valid")
        
        topup_btn = ctk.CTkButton(
            topup_window,
            text="Top Up",
            command=process_topup
        )
        topup_btn.pack(pady=20)
    
    def show_all_transactions(self):
        messagebox.showinfo("Riwayat Transaksi", "Fitur riwayat lengkap akan segera tersedia!")
    
    def show_academic_details(self):
        messagebox.showinfo("Detail Akademik", "Fitur detail akademik akan segera tersedia!")
    
    def show_curriculum(self):
        messagebox.showinfo("Kurikulum", "Fitur kurikulum lengkap akan segera tersedia!")

if __name__ == "__main__":
    app = UserProfile()
    app.mainloop()
