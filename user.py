import os
import json
from abc import ABC, abstractmethod

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.json")
try:
    data = json.load(open(DATA_PATH))
except FileNotFoundError:
    print("File not found")

users_list = data.get("users", [])


class Account(ABC):
    def __init__(self):
        self.username = ""
        self.role = ""
        self.prodi = ""
        self.angkatan = ""
    @abstractmethod
    def addUserToJson(self, user_data):
        pass
    # @abstractmethod
    # def updateJson(self):
    #     pass
    
class Tutor(Account):
    # Atribut
    def __init__(self):
        super().__init__()
        self.role = "tutor"
        self.tutors_list = data.get("tutors", [])
    # Method
    def addUserToJson(self, user_data):
        if "tutor" not in data:
            data["tutor"] = []
        for tutor in self.tutors_list:
            if tutor.get("nama") == user_data.get("nama"):
                return False
        
        data["tutor"].append(user_data)
        with open(DATA_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    
    def getUserByUsername(self, username):
        for tutor in self.tutors_list:
            if tutor.get("nama") == username:
                self.username = tutor.get("nama")
                self.role = tutor.get("role")
                self.harga = int(tutor.get("harga", 0))
                self.prodi = tutor.get("prodi", "")
                self.angkatan = tutor.get("angkatan", "")
                return tutor
        return None
    
    def filterByMatkul(self, matkul):
        return [tutor for tutor in self.loadAllTutors() if matkul in tutor.get("mata-kuliah", [])]
    
    def loadAllTutors(self):
        return data.get("tutor", [])
    

class User(Account, ABC):
    # Atribut
    def __init__(self):
        super().__init__()
        self.role = "student"
        self.saldo = 0
    # Method
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
    
    def transfer_ke_tutor(self, tutor_data):
        if self.saldo >= tutor_data.get("harga", 0):
            for user in data.get("users", []):
                if user.get("username") == tutor_data.get("nama"):
                    user["saldo"] = user.get("saldo", 0) + tutor_data.get("harga", 0)
                    break
            self.saldo -= tutor_data.get("harga", 0)
            self.updateJson()
    
    def topup_saldo(self, amount):
        if amount > 0:
            self.saldo += amount
            self.updateJson()
            return True
        return False    