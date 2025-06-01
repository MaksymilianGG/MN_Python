import json
import os
from utils import validate_string
from logger import Logger

class AuthManager:
    def __init__(self):
        self.users_file = "users.json"
        self.users = self.load_users()
        self.logger = Logger()

        if not self.users:
            self.register_user("admin", "admin123", "manager")
            self.register_user("seller1", "seller123", "seller")

    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except Exception as e:
                self.logger.log(f"Помилка завантаження користувачів: {e}")
                return {}
        return {}

    def save_users(self):
        try:
            with open(self.users_file, "w", encoding="utf-8") as file:
                json.dump(self.users, file, ensure_ascii=False, indent=4)
        except Exception as e:
            self.logger.log(f"Помилка збереження користувачів: {e}")

    def register_user(self, login, password, role):
        if not validate_string(login) or not validate_string(password):
            return False, "Невірний логін або пароль"
        if login in self.users:
            return False, "Користувач уже існує"
        if role not in ["manager", "seller"]:
            return False, "Невірна роль"

        self.users[login] = {"password": password, "role": role}
        self.save_users()
        self.logger.log(f"Зареєстровано користувача: {login} ({role})")
        return True, "Користувача зареєстровано"

    def authenticate(self, login, password):
        if login in self.users and self.users[login]["password"] == password:
            self.logger.log(f"Успішний вхід: {login}")
            return {"login": login, "role": self.users[login]["role"]}
        self.logger.log(f"Невдалий вхід: {login}")
        return None