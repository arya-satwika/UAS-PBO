import customtkinter as ctk
from tkinter import messagebox
import json

users = json.load(open("data.json"))

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

class RegisterTutor(ctk.CTk):
    def __init__(self, master):
        super().__init__()
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
        self.mainFrame.grid(row=0,column=1,pady=20, padx=(5,0), sticky="nsew")
        self.mainFrame.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)

        self.tutors = User().loadAllTutors()
        # ctk.set_widget_scaling(1.)
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
        sidebarFrame.grid(row=0,column=0,pady=20, padx=(20,5), sticky="nsew")
        testlabel= ctk.CTkLabel(
            master=sidebarFrame,
            text="Sidebar",
            font=("Arial", 20, "bold"),
            fg_color="#2dbe10",
            bg_color="#771818",
        )
        testlabel.grid(row=0,column=0,pady=20, padx=20)
    def tutorCard(self, tutor):
        card = ctk.CTkFrame(
            master=self.mainFrame, 
            width=700,  
            height=250,
            fg_color="#029b26",
            corner_radius=40,
        )
        card.pack(pady=10, padx=10, side="top", anchor="n", fill="x")
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
        button_chat = ctk.CTkButton(
            master=card, 
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
        button_chat.grid(row=0,column=1,pady=10, padx=0, sticky="nsew")
    def run(self):
        self.mainloop()
    
if __name__ == "__main__":
    user = User()
    # register=RegisterTutor()
    gui = GUI()
    gui.run()
