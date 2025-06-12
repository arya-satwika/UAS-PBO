import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
try:
    data = json.load(open(DATA_PATH))
except FileNotFoundError:
    print("File not found")

users_list = data.get("users", [])
tutors_list = data.get("tutors", [])

class User:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.role = ""
        self.saldo = 0
        self.prodi = ""
        self.angkatan = ""
    def addUserToJson(self, user_data):
        if "users" not in data:
            data["users"] = []
        for users in users_list:
            if users.get("username") == user_data.get("username"):
                return False
        
        data["users"].append(user_data)
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    def loadAllTutors(self):
        return data.get("tutor", [])
    
    def getUserByUsername(self, username):
        for user in users_list:
            if user.get("username") == username:
                self.username = user.get("username")
                self.password = user.get("password")
                self.role = user.get("role")
                self.saldo = int(user.get("saldo", 0))
                self.prodi = user.get("prodi", "")
                self.angkatan = user.get("angkatan", "")

        return None
    def filterByMatkul(self, matkul):
        return [tutor for tutor in self.loadAllTutors() if matkul in tutor.get("mata-kuliah", [])]
    
    def authUser(self, username, password):
        for user in users_list:
            if user.get("username") == username and user.get("password") == password:
                self.username = user.get("username")
                self.password = user.get("password")
                self.saldo = int(user.get("saldo", 0))
                self.role = user.get("role")
                self.prodi = user.get("prodi", "")
                self.angkatan = user.get("angkatan", "")
                return True
        return False
    
    def updateJson(self):
        for user in data.get("users", []):
            if user.get("username") == self.username:
                user["password"] = self.password
                user["role"] = self.role
                user["saldo"] = self.saldo
                user["prodi"] = self.prodi
                user["angkatan"] = self.angkatan
                break
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f, indent=4)
    
    def register_tutor(self, harga, matkul, waktu_belajar, tempat_belajar):
        data["tutor"].append({
            "nama": self.username,
            "prodi": self.prodi,
            "angkatan": self.angkatan,
            "tempat-belajar": tempat_belajar,
            "waktu-belajar": waktu_belajar,
            "mata-kuliah": [matkul],
            "harga": harga
        })
    def transfer_ke_tutor(self, tutor):
        if self.saldo >= tutor.get("harga", 0):
            for t in tutors_list:
                if t.get("nama") == tutor.get("nama"):
                    for user in users_list:
                        if user.get("username") == tutor.get("nama"):
                            user["saldo"] = user.get("saldo", 0) + tutor.get("harga", 0)
                            break
                    self.saldo -= tutor.get("harga", 0)
                    self.updateJson()
    
    def topup_saldo(self, amount):
        if amount > 0:
            self.saldo += amount
            self.updateJson()
            return True
        return False    