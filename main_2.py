import os
import json
import customtkinter as ctk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
PAYMENT_PATH = os.path.join(BASE_DIR, "payment.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    users = json.load(f)

def save_payment(data):
    try:
        with open(PAYMENT_PATH, "r", encoding="utf-8") as f:
            payment = json.load(f)
    except FileNotFoundError:
        payment = []

    payment.append(data)
    with open(PAYMENT_PATH, "w", encoding="utf-8") as f:
        json.dump(payment, f, indent=4)

class User:
    def __init__(self):
        self.tutors=self.loadAllTutors()
    def loadAllTutors(self):
        user_list = users.get("tutor", [])
        return user_list
    def filterByMatkul(self, matkul):
        filtered_list = []
        for filtered_user in self.tutors:
            if matkul in filtered_user.get("matkul", []):
                filtered_list.append(filtered_user)
        return filtered_list
    def printAllTutors(self):
        for user in users.get("tutor", []):
            print(list(user.values()))



class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tutor App")
        self.geometry("900x500")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Tambahkan sidebarFrame sebelum sidebar() dipanggil
        self.sidebarFrame = ctk.CTkFrame(
            master=self,
            width=200,
            height=500,
            fg_color="#2dbe10",
            bg_color="#771818",
            corner_radius=20,
        )
        self.sidebarFrame.grid(row=0, column=0, pady=20, padx=(20,5), sticky="nsew")
        self.mainFrame = ctk.CTkScrollableFrame(
            master=self,
            fg_color="#ba2525",
            width=700,
            height=500,
            )
        self.mainFrame.grid(row=0, column=1, pady=20, padx=(5,0), sticky="nsew")
        self.mainFrame.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.tutors = User().loadAllTutors()
        # ctk.set_widget_scaling(1.)
        ctk.set_default_color_theme("green")
      
        self.sidebar()
        for tutor in self.tutors:
            # Pastikan field email ada, jika tidak tambahkan default
            if "email" not in tutor:
                tutor["email"] = "-"
            self.tutorCard(tutor)
    
    def sidebar(self):
        titleLabel= ctk.CTkLabel(
            master=self.sidebarFrame,
            text="Tutor App",
            font=("Roboto Mono", 20, "bold"),
            fg_color="#2dbe10",
            bg_color="#771818",
        )
        titleLabel.grid(row=0,column=0,pady=20, padx=20)
        buttonFrame = ctk.CTkFrame(
            master=self.sidebarFrame, 
            width=200, 
            height=50,
            fg_color="#2dbe10",
            bg_color="#771818",
            corner_radius=20,
        )
        buttonFrame.grid(row=1,column=0, pady=10, padx=20)
        buttonHistory= ctk.CTkButton(
            master=buttonFrame, 
            text="History", 
            font=("Arial", 16),
            command=lambda: print("History clicked"),
            corner_radius=20,
            height=40,
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049",
            bg_color="#2dbe10",
        )
        buttonHistory.pack(side="top", pady=10, padx=10, fill="x")
        # Hapus duplikasi buttonFrame dan buttonHistory
        # Tambahkan tombol Register Tutor yang benar
        buttonRegisterTutor = ctk.CTkButton(
            master=self.sidebarFrame,
            text="Register Tutor",
            font=("Arial", 16),
            command=self.open_register_tutor,
            corner_radius=20,
            height=40,
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049",
            bg_color="#2dbe10",
        )
        buttonRegisterTutor.grid(row=2, column=0, pady=10, padx=10, sticky="ew")
    
    def open_register_tutor(self):

        self.mainFrame.grid_forget()
        self.sidebarFrame.grid_forget()
        self.withdraw()
        win = ctk.CTkToplevel(self)
        win.title("Register Tutor")
        win.state("zoomed")
        
        label_nama = ctk.CTkLabel(win, text="Nama Pengajar:")
        label_nama.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_nama = ctk.CTkEntry(win)
        entry_nama.grid(row=0, column=1, padx=10, pady=5)

        label_prodi = ctk.CTkLabel(win, text="Prodi:")
        label_prodi.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_prodi = ctk.CTkEntry(win)
        entry_prodi.grid(row=1, column=1, padx=10, pady=5)

        label_angkatan = ctk.CTkLabel(win, text="Angkatan:")
        label_angkatan.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_angkatan = ctk.CTkEntry(win)
        entry_angkatan.grid(row=2, column=1, padx=10, pady=5)

        label_matkul = ctk.CTkLabel(win, text="Mata Kuliah yang Dikuasai (pisahkan dengan koma):")
        label_matkul.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        entry_matkul = ctk.CTkEntry(win)
        entry_matkul.grid(row=3, column=1, padx=10, pady=5)

        label_tempat = ctk.CTkLabel(win, text="Tempat Belajar:")
        label_tempat.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        entry_tempat = ctk.CTkEntry(win)
        entry_tempat.grid(row=4, column=1, padx=10, pady=5)

        label_waktu = ctk.CTkLabel(win, text="Waktu Belajar:")
        label_waktu.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        entry_waktu = ctk.CTkEntry(win)
        entry_waktu.grid(row=5, column=1, padx=10, pady=5)

        def do_register():
            nama = entry_nama.get().strip()
            prodi = entry_prodi.get().strip()
            angkatan = entry_angkatan.get().strip()
            mata_kuliah = entry_matkul.get().strip()
            tempat_belajar = entry_tempat.get().strip()
            waktu_belajar = entry_waktu.get().strip()
            if not nama or not prodi or not angkatan or not mata_kuliah or not tempat_belajar or not waktu_belajar:
                messagebox.showerror("Error", "Semua field harus diisi!")
                return
            try:
                angkatan_int = int(angkatan)
            except ValueError:
                messagebox.showerror("Error", "Angkatan harus berupa angka!")
                return
            tutor_data = {
                "nama": nama,
                "prodi": prodi,
                "angkatan": angkatan_int,
                "mata-kuliah": [m.strip() for m in mata_kuliah.split(",")],
                "tempat-belajar": tempat_belajar,
                "waktu-belajar": waktu_belajar,
                "email": "-"  # Tambahkan field email agar tidak error
            }
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.setdefault("tutor", []).append(tutor_data)
            with open(DATA_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            messagebox.showinfo("Sukses", f"Pengajar {nama} berhasil didaftarkan!")
            entry_nama.delete(0, ctk.END)
            entry_prodi.delete(0, ctk.END)
            entry_angkatan.delete(0, ctk.END)
            entry_matkul.delete(0, ctk.END)
            entry_tempat.delete(0, ctk.END)
            entry_waktu.delete(0, ctk.END)
            # Tampilkan kembali window utama dan frame setelah register
            win.destroy()
            self.deiconify()
            self.mainFrame.grid(row=0,column=1,pady=20, padx=(5,20), sticky="nsew",rowspan=2)
            self.sidebarFrame.grid(row=0,column=0,pady=20, padx=(20,5), sticky="nsew",rowspan=2)

        button_register = ctk.CTkButton(win, text="Register", command=do_register)
        button_register.grid(row=6, column=0, columnspan=2, pady=20)

        def kembali():
            win.destroy()
            self.deiconify()
            self.mainFrame.grid(row=0,column=1,pady=20, padx=(5,20), sticky="nsew",rowspan=2)
            self.sidebarFrame.grid(row=0,column=0,pady=20, padx=(20,5), sticky="nsew",rowspan=2)

        button_kembali = ctk.CTkButton(win, text="Kembali", command=kembali)
        button_kembali.grid(row=7, column=0, columnspan=2, pady=10)
       
    def tutorCard(self, tutor):
        card = ctk.CTkFrame(
            master=self.mainFrame, 
            width=700,  
            height=250,
            fg_color="#029b26",
            corner_radius=40,
        )
        card.pack(pady=10, padx=10, side="top", anchor="n", fill="x")
        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=0)
        namaTutor = ctk.CTkLabel(
            master=card, 
            text=f"{tutor['nama']}", 
            font=("Gotham", 24, "bold"),
            anchor="w",
            justify="left",
            bg_color="blue",
        )
        namaTutor.grid(row=0,column=0,padx=10, pady=5, sticky="w")
        frame_matkul= ctk.CTkFrame(
            master=card, 
            width=200, 
            height=50,
            bg_color="red",
            fg_color="red",
            corner_radius=400,
        )
        frame_matkul.grid(row=1,column=0,pady=0, padx=0,sticky="w")
        matkul_label = ctk.CTkLabel(
            master=frame_matkul, 
            width=20,
            text=f"Mata Kuliah: {', '.join(tutor['mata-kuliah'])}", 
            font=("Arial", 16),
            anchor="w",
            justify="left",
            wraplength=400,
            bg_color="blue",
        )
        matkul_label.grid(row=0,column=0,padx=10, pady=10, sticky="w",)
        inner_frame = ctk.CTkFrame(
            master=card,
            width=200,
            height=100,
            bg_color="#5ad6ff",
            fg_color="#5ad6ff",
            corner_radius=20,
        )
        inner_frame.grid(row=2,column=0,pady=0, padx=0, sticky="ew")
        waktu_label = ctk.CTkLabel(
            master=inner_frame, 
            text=f"Waktu Belajar: {tutor['waktu-belajar']}", 
            font=("Arial", 16),
            anchor="w",
            justify="left",
            bg_color="blue",
        )
        waktu_label.pack(padx=(10,5), pady=0,side="left")
        tempat_label = ctk.CTkLabel(
            master=inner_frame, 
            text=f"Tempat Belajar: {tutor['tempat-belajar']}", 
            font=("Arial", 16),
            anchor="w",
            justify="left",
            bg_color="blue",
        )
        tempat_label.pack(padx=5, pady=0,side="left")
        buttonFrame = ctk.CTkFrame(
            master=card, 
            width=200, 
            height=50,
            bg_color="#4C74AF",
            fg_color="#4C74AF",
            corner_radius=20,
        )
        buttonFrame.grid(row=3,column=1,pady=10, padx=10, sticky="ew")
        button_chat = ctk.CTkButton(
            master=buttonFrame, 
            text="Chat", 
            font=("Arial", 16),
            command=lambda: print(f"Chat with {tutor['nama']}"),
            corner_radius=20,
            height=40,
            width=100,
            fg_color="#4CAF50",
            hover_color="#45a049",
            bg_color="#4C74AF",
        )
        button_chat.grid(row=0,column=3,pady=10, padx=0, sticky="w")

        button_bayar = ctk.CTkButton(
            master=buttonFrame,
            text="Bayar",
            font=("Arial", 16),
            command=lambda: self.make_payment(tutor),
            corner_radius=20,
            height=40,
            width=100,
            fg_color="#e67e22",
            hover_color="#d35400",
            bg_color="#4C74AF",
        )
        button_bayar.grid(row=0,column=4,pady=10, padx=(10,0), sticky="e")
    
    def make_payment(self, tutor):
        payment_window = ctk.CTkToplevel(self)
        payment_window.title("Form Pembayaran")
        payment_window.geometry("400x250")

        label_info = ctk.CTkLabel(
            master=payment_window,
            text=f"Pembayaran untuk: {tutor['nama']}",
            font=("Arial", 18)
        )
        label_info.pack(pady=15)

        entry_nominal = ctk.CTkEntry(
            master=payment_window,
            placeholder_text="Masukkan nominal pembayaran (Rp)",
            font=("Arial", 14)
        )
        entry_nominal.pack(pady=10)

        def submit_payment():
            nominal = entry_nominal.get()
            if not nominal.isdigit():
                messagebox.showerror("Error", "Nominal harus berupa angka.")
                return
            data = {
                "tutor": tutor["nama"],
                "email": tutor.get("email", "-"),
                "amount": int(nominal)
            }
            save_payment(data)
            messagebox.showinfo("Sukses", f"Pembayaran Rp{nominal} berhasil disimpan!")
            payment_window.destroy()

        submit_btn = ctk.CTkButton(
            master=payment_window,
            text="Bayar",
            fg_color="green",
            hover_color="#157a18",
            command=submit_payment
        )
        submit_btn.pack(pady=15)

    def run(self):
        self.mainloop()
    
if __name__ == "__main__":
    # user = User()  # Tidak perlu instance User di sini
    gui = GUI()
    gui.run()
