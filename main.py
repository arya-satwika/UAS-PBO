import json

users = json.load(open("data.json"))

class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.loadUsers()
    def loadAllUsers(self):
        user_list = users.get("users", [])
        return user_list
    def filterByMatkul(self, matkul):
        filtered_list = [
            filtered_user 
            for filtered_user in users.get("users", [])
                if matkul in filtered_user.get("matkul", [])]
        return filtered_list
class matkul:
    def __init__(self, name, code):
        self.name = name
        self.code = code

