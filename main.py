import json
import customtkinter as ctk

users = json.load(open("data.json"))

class User:
    def __init__(self):
        self.loadAllTutors()
    def loadAllTutors(self):
        user_list = users.get("tutor", [])
        return user_list
    def filterByMatkul(self, matkul):
        filtered_list = [
            filtered_user
            for filtered_user in users.get("tutor", [])
                if matkul in filtered_user.get("matkul", [])]
        return filtered_list
    def printAllTutors(self):
        for user in users.get("tutor", []):
            print(list(user.values()))

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Tutor App")
        self.geometry("1200x800")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # self.minsize(1000, 700)
        self.frame = ctk.CTkScrollableFrame(master=self,fg_color="#ba2525")
        self.frame.grid(row=0,column=0,pady=20, padx=20, sticky="nsew")
        # self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure((0, 1), weight=1)
        self.tutors = {
            "nama": "Astuti",
            "angkatan": 2022,
            "prodi": "Teknik Informatika",
            "tempat-belajar": "FC Ketintang",
            "waktu-belajar": "15.00 - 17.00",
            "mata-kuliah": [
                "Struktur Data", 
                "Pemrograman Berorientasi Objek",
                "Statistika",
                "Matetmatika Diskrit"
            ]
        }
        
        ctk.set_widget_scaling(1.5)
        ctk.set_default_color_theme("green")
        for tutor in users.get("tutor", []):
            self.tutorCard(tutor)
        self.tutorCard(self.tutors)
    
    def tutorCard(self, tutor):
        card = ctk.CTkFrame(
            master=self.frame, 
            width=1200,  
            height=250,
            fg_color="#029b26",
            corner_radius=40,
        )
        card.pack(pady=20, padx=20, expand=True,side="top", anchor="n")
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
        )
        button_chat.grid(row=0,column=1,pady=10, padx=10)
        button_chat.grid_columnconfigure(1, weight=1)
    def run(self):
        self.mainloop()
    
if __name__ == "__main__":
    user = User()
    gui = GUI()
    gui.run()