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
        # self.minsize(1000, 700)
        self.frame = ctk.CTkFrame(master=self,fg_color="#2e4a5c")
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.grid_columnconfigure((0, 1), weight=1)
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
        self.tutorCard(self.tutors)
    
    def tutorCard(self, tutor):
        card = ctk.CTkFrame(
            master=self.frame, 
            width=500,  
            height=250,
            fg_color="#132e3f",
            corner_radius=40,
        )
        card.grid(row=0,column=0,pady=20, padx=20, sticky="nsew")
        namaTutor = ctk.CTkLabel(
            master=card, 
            text=f"{tutor['nama']}", 
            font=("Arial", 24),
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

    def run(self):
        self.mainloop()
    
if __name__ == "__main__":
    user = User()
    gui = GUI()
    gui.run()