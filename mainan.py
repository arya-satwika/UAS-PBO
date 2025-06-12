import os
import json
import customtkinter as ctk # 
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
PAYMENT_PATH = os.path.join(BASE_DIR, "payment.json") 
users = json.load(open(DATA_PATH))

def save_payment(data):
    try:
        with open(PAYMENT_PATH, "r") as f:
            payment = json.load(f)
    except FileNotFoundError:
        payment = []

    payment.append(data)
    with open(PAYMENT_PATH, "w") as f:
        json.dump(payment, f, indent=4)

class User:
    def __init__(self, name=None, saldo=None, email=None, matkul=None):
        self.name = name
        self.saldo = saldo
        self.email = email
        self.matkul = matkul
        self.tutors = self.loadAllTutors()
        
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
    
    def add_tutor(self):
        if "tutor" not in users:
            users["tutor"] = []
        users["tutor"].append({
            "nama": self.name,
            "saldo": self.saldo,
            "email": self.email,
            "matkul": [self.matkul]
        })
        with open(DATA_PATH, "w") as f:
            json.dump(users, f, indent=4)

class RegisterTutor(ctk.CTk):
    def __init__(self, master):
        super().__init__()
        self.title("Tutor App")
        self.geometry("900x500")

        self.saldo_user = 100000

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.master = master
        master.title("TutorCerdas")

        self.label_name = ctk.CTkLabel(master, text="Nama Pengajar:")
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entry_name = ctk.CTkEntry(master)
        self.entry_name.grid(row=0, column=1, padx=10, pady=5)

        self.label_email = ctk.CTkLabel(master, text="Email:")
        self.label_email.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_email = ctk.CTkEntry(master)
        self.entry_email.grid(row=1, column=1, padx=10, pady=5)

        self.label_matkul = ctk.CTkLabel(master, text="Mata Kuliah:")
        self.label_matkul.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_matkul = ctk.CTkEntry(master)
        self.entry_matkul.grid(row=2, column=1, padx=10, pady=5)

        self.button_register = ctk.CTkButton(master, text="Register", command=self.register_tutor)
        self.button_register.grid(row=3, column=0, columnspan=2, pady=10)

    def register_tutor(self):
        name = self.entry_name.get()
        email = self.entry_email.get()
        matkul = self.entry_matkul.get()

        if not name or not email or not matkul:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        user = User(name, 0, email, matkul)
        user.add_tutor()

        messagebox.showinfo("Sukses", f"Pengajar {name} berhasil didaftarkan!")
        self.entry_name.delete(0, ctk.END)
        self.entry_email.delete(0, ctk.END)
        self.entry_matkul.delete(0, ctk.END)

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tutor App")
        self.geometry("900x500")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
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
        self.saldo_user = 100000  # Added missing attribute
        ctk.set_default_color_theme("green")
      
        self.sidebar()
        for tutor in self.tutors:
            self.tutorCard(tutor)
    
    def sidebar(self):
        sidebarFrame = ctk.CTkFrame(
            master=self, 
            width=200, 
            height=500,
            fg_color="#2dbe10",
            bg_color="#771818",
            corner_radius=20,
        )
        sidebarFrame.grid(row=0, column=0, pady=20, padx=(20,5), sticky="nsew")
        testlabel = ctk.CTkLabel(
            master=sidebarFrame,
            text="Sidebar",
            font=("Arial", 20, "bold"),
            fg_color="#2dbe10",
            bg_color="#771818",
        )
        testlabel.grid(row=0, column=0, pady=20, padx=20)
    
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
        namaTutor.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        frame_matkul = ctk.CTkFrame(
            master=card, 
            width=200, 
            height=50,
            bg_color="red",
            fg_color="red",
            corner_radius=400,
        )
        
        harga_label = ctk.CTkLabel(
            master=card,
            text=f"Harga: Rp{tutor['harga']}",
            font=("Arial", 16),
            anchor="w",
            justify="left",
            bg_color="blue",
        )
        harga_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        frame_matkul.grid(row=1, column=0, pady=0, padx=0, sticky="w")
        
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
        matkul_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        inner_frame = ctk.CTkFrame(
            master=card,
            width=200,
            height=100,
            bg_color="#5ad6ff",
            fg_color="#5ad6ff",
            corner_radius=20,
        )
        inner_frame.grid(row=2, column=0, pady=0, padx=0, sticky="ew")
        
        waktu_label = ctk.CTkLabel(
            master=inner_frame, 
            text=f"Waktu Belajar: {tutor['waktu-belajar']}", 
            font=("Arial", 16),
            anchor="w",
            justify="left",
            bg_color="blue",
        )
        waktu_label.pack(padx=(10,5), pady=0, side="left")
        
        tempat_label = ctk.CTkLabel(
            master=inner_frame, 
            text=f"Tempat Belajar: {tutor['tempat-belajar']}", 
            font=("Arial", 16),
            anchor="w",
            justify="left",
            bg_color="blue",
        )
        tempat_label.pack(padx=5, pady=0, side="left")
        
        buttonFrame = ctk.CTkFrame(
            master=card, 
            width=200, 
            height=50,
            bg_color="#4C74AF",
            fg_color="#4C74AF",
            corner_radius=20,
        )
        buttonFrame.grid(row=3, column=0, columnspan=2, pady=10, sticky="e")

        button_bayar = ctk.CTkButton(
            master=buttonFrame,
            text="Bayar",
            font=("Arial", 16),
            command=lambda: self.handle_chat(tutor_data),
            corner_radius=20,
            height=40,
            width=100,
            fg_color="#e67e22",
            hover_color="#d35400",
            bg_color="#4C74AF",
        )
        button_bayar.grid(row=0, column=0, pady=10, padx=(10,0), sticky="e")
    
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

        def handle_chat(self, tutor_data):
            harga = tutor_data.get('harga', 0)
    
            if self.saldo_user < harga:
               messagebox.showwarning("Saldo Tidak Cukup", 
                                    f"Saldo Anda tidak mencukupi untuk membayar Rp{harga}")
               return
    
    
            confirm = messagebox.askyesno(
                "Konfirmasi Pembayaran",
                 f"Anda akan membayar Rp{harga} untuk chat dengan {tutor_data['nama']}.\nLanjutkan?"
            )
    
            if confirm:
               self.saldo_user -= harga
               save_payment({
                    "tutor": tutor_data['nama'],
                    "amount": harga,
                "type": "chat"
               })
        
        
               self.open_chat_window(tutor_data)

        def open_chat_window(self, tutor_data):
            chat_window = ctk.CTkToplevel(self)
            chat_window.title(f"Chat dengan {tutor_data['nama']}")
            chat_window.geometry("500x600")
    
    
            chat_frame = ctk.CTkScrollableFrame(chat_window)
            chat_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    
            example_messages = [
               {"sender": tutor_data['nama'], "text": "Halo! Ada yang bisa saya bantu?"},
               {"sender": "Anda", "text": "Saya ingin bertanya tentang materi..."}
    ]
    

            for msg in example_messages:
                frame = ctk.CTkFrame(chat_frame, corner_radius=10)
                frame.pack(fill="x", padx=5, pady=5)
        
                label = ctk.CTkLabel(
                    frame,
                    text=f"{msg['sender']}: {msg['text']}",
                    wraplength=400,
                    justify="left"
                )
                label.pack(padx=10, pady=5, anchor="w")
    
   
            input_frame = ctk.CTkFrame(chat_window, height=60)
            input_frame.pack(fill="x", padx=10, pady=10)
    
            entry = ctk.CTkEntry(input_frame, placeholder_text="Ketik pesan...")
            entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
            def send_message():
                message = entry.get()
                if message:
            
                   frame = ctk.CTkFrame(chat_frame, corner_radius=10)
                   frame.pack(fill="x", padx=5, pady=5)
            
                   label = ctk.CTkLabel(
                       frame,
                       text=f"Anda: {message}",
                       wraplength=400,
                       justify="left"
                    )
                   label.pack(padx=10, pady=5, anchor="w")
            
                   entry.delete(0, "end")
    
            send_btn = ctk.CTkButton(
                 input_frame,
                 text="Kirim",
                 width=80,
                 command=send_message
             )
            send_btn.pack(side="right")

        def submit_payment():
            nominal = entry_nominal.get()
            if not nominal.isdigit():
                messagebox.showerror("Error", "Nominal harus berupa angka.")
                return
            
            nominal_int = int(nominal)
            if self.saldo_user < nominal_int:
                messagebox.showerror("Error", "Saldo tidak mencukupi!")
                return
                
            self.saldo_user -= nominal_int
            data = {
                "tutor": tutor["nama"],
                "amount": nominal_int
            }
            save_payment(data)
            messagebox.showinfo("Sukses", f"Pembayaran Rp{nominal} berhasil disimpan!\nSaldo tersisa: Rp{self.saldo_user}")
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
    gui = GUI()
    gui.run()