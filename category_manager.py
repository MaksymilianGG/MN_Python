from logger import Logger

class CategoryManager:
    def __init__(self):
        self.categories = ["Електроніка", "Одяг", "Продукти", "Інше"]
        self.logger = Logger()

    def get_categories(self):
        return self.categories

    def add_category(self, category):
        if category and category not in self.categories:
            self.categories.append(category)
            self.logger.log(f"Додано категорію: {category}")
            return True, "Категорію додано"
        self.logger.log(f"Невдала спроба додати категорію: {category}")
        return False, "Категорія вже існує або невалідна"

    def remove_category(self, category):
        if category in self.categories and category != "Інше":
            self.categories.remove(category)
            self.logger.log(f"Видалено категорію: {category}")
            return True, "Категорію видалено"
        self.logger.log(f"Невдала спроба видалити категорію: {category}")
        return False, "Категорію не можна видалити"