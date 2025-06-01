import json
import os
from datetime import datetime
from utils import validate_number, format_currency
from logger import Logger


class InventoryManager:
    def __init__(self):
        self.inventory_file = "inventory.json"
        self.inventory = self.load_inventory()
        self.categories = self.load_categories()
        self.logger = Logger()

    def load_inventory(self):
        if os.path.exists(self.inventory_file):
            try:
                with open(self.inventory_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    # Переконуємося, що всі необхідні ключі присутні
                    if "products" not in data:
                        data["products"] = {}
                    if "transactions" not in data:
                        data["transactions"] = []
                    if "history" not in data:
                        data["history"] = {}

                    # Нормалізація транзакцій: додаємо ключ 'user', якщо його немає
                    for transaction in data["transactions"]:
                        if "user" not in transaction:
                            transaction["user"] = "unknown"

                    # Додаємо low_stock_alert для всіх товарів, якщо відсутній
                    for product in data["products"].values():
                        if "low_stock_alert" not in product:
                            product["low_stock_alert"] = product.get("quantity", 0) < 5

                    return data
            except Exception as e:
                self.logger.log(f"Помилка завантаження інвентарю: {e}")
                return {"products": {}, "transactions": [], "history": {}}
        return {"products": {}, "transactions": [], "history": {}}

    def save_inventory(self):
        try:
            with open(self.inventory_file, "w", encoding="utf-8") as file:
                json.dump(self.inventory, file, ensure_ascii=False, indent=4)
        except Exception as e:
            self.logger.log(f"Помилка збереження інвентарю: {e}")

    def load_categories(self):
        return ["Електроніка", "Одяг", "Продукти", "Інше"]

    def add_product(self, name, quantity, price, category, user):
        if not name or not validate_number(quantity, min_val=0) or not validate_number(price, min_val=0):
            self.logger.log(f"Невірні дані товару: {name}, {quantity}, {price}")
            return False, "Невірні дані товару"

        if name in self.inventory["products"]:
            self.logger.log(f"Спроба додати існуючий товар: {name}")
            return False, "Товар уже існує"

        self.inventory["products"][name] = {
            "quantity": int(quantity),
            "price": float(price),
            "category": category,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "low_stock_alert": int(quantity) < 5
        }
        self.add_transaction("add", name, int(quantity), float(price), user)
        self.add_history(name, f"Додано товар: {quantity} шт, ціна {format_currency(price)}", user)
        self.save_inventory()
        self.logger.log(f"Додано товар: {name}, {quantity} шт, {format_currency(price)}")
        return True, "Товар додано успішно"

    def receive_product(self, name, quantity, user):
        if name not in self.inventory["products"]:
            self.logger.log(f"Товар не знайдено для надходження: {name}")
            return False, "Товар не знайдено"
        if not validate_number(quantity, min_val=1):
            self.logger.log(f"Невірна кількість для надходження: {quantity}")
            return False, "Невірна кількість"

        self.inventory["products"][name]["quantity"] += int(quantity)
        self.inventory["products"][name]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.inventory["products"][name]["low_stock_alert"] = self.inventory["products"][name]["quantity"] < 5
        self.add_transaction("receive", name, int(quantity), self.inventory["products"][name]["price"], user)
        self.add_history(name, f"Надходження: {quantity} шт", user)
        self.save_inventory()
        self.logger.log(f"Надходження товару: {name}, {quantity} шт")
        return True, "Надходження зареєстровано"

    def sell_product(self, name, quantity, user):
        if name not in self.inventory["products"]:
            self.logger.log(f"Товар не знайдено для продажу: {name}")
            return False, "Товар не знайдено"
        if not validate_number(quantity, min_val=1):
            self.logger.log(f"Невірна кількість для продажу: {quantity}")
            return False, "Невірна кількість"
        if self.inventory["products"][name]["quantity"] < int(quantity):
            self.logger.log(f"Недостатньо товару: {name}, залишок {self.inventory['products'][name]['quantity']}")
            return False, "Недостатньо товару на складі"

        self.inventory["products"][name]["quantity"] -= int(quantity)
        self.inventory["products"][name]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.inventory["products"][name]["low_stock_alert"] = self.inventory["products"][name]["quantity"] < 5
        self.add_transaction("sell", name, int(quantity), self.inventory["products"][name]["price"], user)
        self.add_history(name, f"Продаж: {quantity} шт", user)
        self.save_inventory()
        self.logger.log(f"Продаж товару: {name}, {quantity} шт")
        return True, "Продаж зареєстровано"

    def add_transaction(self, action, name, quantity, price, user):
        transaction = {
            "action": action,
            "name": name,
            "quantity": quantity,
            "price": price,
            "total": quantity * price,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user["login"]
        }
        self.inventory["transactions"].append(transaction)

    def add_history(self, name, change, user):
        if name not in self.inventory["history"]:
            self.inventory["history"][name] = []
        self.inventory["history"][name].append({
            "change": change,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": user["login"]
        })

    def get_inventory(self):
        return self.inventory["products"]

    def get_transactions(self):
        return self.inventory["transactions"]

    def get_history(self, name):
        return self.inventory["history"].get(name, [])

    def get_categories(self):
        return self.categories

    def get_total_value(self):
        return sum(details["quantity"] * details["price"] for details in self.inventory["products"].values())