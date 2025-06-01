import customtkinter as ctk
from tkinter import messagebox
from styles import FONT, BUTTON_WIDTH, ENTRY_WIDTH
from inventory_manager import InventoryManager
from utils import format_currency, validate_string
from category_manager import CategoryManager

class InventoryGUI:
    def __init__(self, root, inventory_manager: InventoryManager, user):
        self.root = root
        self.inventory_manager = inventory_manager
        self.category_manager = CategoryManager()
        self.user = user
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.setup_top_bar()
        self.tab_view = ctk.CTkTabview(self.main_frame)
        self.tab_view.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.setup_tabs()

    def setup_top_bar(self):
        top_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        top_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(top_frame, text=f"Користувач: {self.user['login']} ({self.user['role']})", font=FONT).grid(row=0, column=0, padx=5)
        ctk.CTkOptionMenu(top_frame, values=["System", "Light", "Dark"], command=lambda x: ctk.set_appearance_mode(x)).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(top_frame, text=f"Вартість інвентарю: {format_currency(self.inventory_manager.get_total_value())}", font=FONT).grid(row=0, column=2, padx=5)

    def setup_tabs(self):
        tabs = ["Додати товар", "Надходження", "Продаж", "Перегляд залишків", "Транзакції"]
        if self.user["role"] == "manager":
            tabs.extend(["Категорії", "Історія"])
        for tab in tabs:
            self.tab_view.add(tab)

        self.setup_add_product_tab()
        self.setup_receive_product_tab()
        self.setup_sell_product_tab()
        self.setup_view_inventory_tab()
        self.setup_transactions_tab()
        if self.user["role"] == "manager":
            self.setup_categories_tab()
            self.setup_history_tab()

    def setup_add_product_tab(self):
        tab = self.tab_view.tab("Додати товар")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")

        if self.user["role"] != "manager":
            ctk.CTkLabel(frame, text="Доступно лише для менеджерів", font=FONT).grid(row=0, column=0, padx=5, pady=5)
            return

        ctk.CTkLabel(frame, text="Назва товару:", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_name_entry = ctk.CTkEntry(frame, width=ENTRY_WIDTH, font=FONT)
        self.add_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Кількість:", font=FONT).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_quantity_entry = ctk.CTkEntry(frame, width=ENTRY_WIDTH, font=FONT)
        self.add_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Ціна (грн):", font=FONT).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.add_price_entry = ctk.CTkEntry(frame, width=ENTRY_WIDTH, font=FONT)
        self.add_price_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Категорія:", font=FONT).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.add_category_combo = ctk.CTkComboBox(frame, values=self.inventory_manager.get_categories(), width=ENTRY_WIDTH, font=FONT)
        self.add_category_combo.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Додати товар", command=self.add_product, width=BUTTON_WIDTH, font=FONT, hover_color="#2ecc71").grid(row=4, column=0, columnspan=2, pady=10)

    def setup_receive_product_tab(self):
        tab = self.tab_view.tab("Надходження")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame, text="Назва товару:", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.receive_name_entry = ctk.CTkComboBox(frame, values=list(self.inventory_manager.get_inventory().keys()), width=ENTRY_WIDTH, font=FONT)
        self.receive_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Кількість:", font=FONT).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.receive_quantity_entry = ctk.CTkEntry(frame, width=ENTRY_WIDTH, font=FONT)
        self.receive_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Зареєструвати надходження", command=self.receive_product, width=BUTTON_WIDTH, font=FONT, hover_color="#2ecc71").grid(row=2, column=0, columnspan=2, pady=10)

    def setup_sell_product_tab(self):
        tab = self.tab_view.tab("Продаж")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame, text="Назва товару:", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.sell_name_entry = ctk.CTkComboBox(frame, values=list(self.inventory_manager.get_inventory().keys()), width=ENTRY_WIDTH, font=FONT)
        self.sell_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkLabel(frame, text="Кількість:", font=FONT).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.sell_quantity_entry = ctk.CTkEntry(frame, width=ENTRY_WIDTH, font=FONT)
        self.sell_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Зареєструвати продаж", command=self.sell_product, width=BUTTON_WIDTH, font=FONT, hover_color="#2ecc71").grid(row=2, column=0, columnspan=2, pady=10)

    def setup_view_inventory_tab(self):
        tab = self.tab_view.tab("Перегляд залишків")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.inventory_tree = ctk.CTkFrame(frame)
        self.inventory_tree.grid(row=1, column=0, sticky="nsew")
        self.update_inventory_view()

        ctk.CTkButton(frame, text="Оновити", command=self.update_inventory_view, width=BUTTON_WIDTH, font=FONT).grid(row=2, column=0, pady=10)

    def setup_transactions_tab(self):
        tab = self.tab_view.tab("Транзакції")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        self.transactions_tree = ctk.CTkFrame(frame)
        self.transactions_tree.grid(row=0, column=0, sticky="nsew")
        self.update_transactions_view()

        ctk.CTkButton(frame, text="Оновити", command=self.update_transactions_view, width=BUTTON_WIDTH, font=FONT).grid(row=1, column=0, pady=10)

    def setup_categories_tab(self):
        tab = self.tab_view.tab("Категорії")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(frame, text="Нова категорія:", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.category_entry = ctk.CTkEntry(frame, width=ENTRY_WIDTH, font=FONT)
        self.category_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Додати категорію", command=self.add_category, width=BUTTON_WIDTH, font=FONT).grid(row=1, column=0, columnspan=2, pady=5)
        ctk.CTkButton(frame, text="Видалити категорію", command=self.remove_category, width=BUTTON_WIDTH, font=FONT).grid(row=2, column=0, columnspan=2, pady=5)

        self.category_list = ctk.CTkFrame(frame)
        self.category_list.grid(row=3, column=0, columnspan=2, pady=5)
        self.update_category_list()

    def setup_history_tab(self):
        tab = self.tab_view.tab("Історія")
        frame = ctk.CTkFrame(tab, corner_radius=10)
        frame.grid(padx=10, pady=10, sticky="nsew")
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame, text="Назва товару:", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.history_name_entry = ctk.CTkComboBox(frame, values=list(self.inventory_manager.get_inventory().keys()), width=ENTRY_WIDTH, font=FONT)
        self.history_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ctk.CTkButton(frame, text="Показати історію", command=self.update_history_view, width=BUTTON_WIDTH, font=FONT).grid(row=0, column=2, padx=5)

        self.history_tree = ctk.CTkFrame(frame)
        self.history_tree.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.update_history_view()

    def add_product(self):
        if self.user["role"] != "manager":
            messagebox.showerror("Помилка", "Доступно лише для менеджерів")
            return
        name = self.add_name_entry.get().strip()
        quantity = self.add_quantity_entry.get().strip()
        price = self.add_price_entry.get().strip()
        category = self.add_category_combo.get()

        success, message = self.inventory_manager.add_product(name, quantity, price, category, self.user)
        messagebox.showinfo("Результат", message) if success else messagebox.showerror("Помилка", message)
        if success:
            self.add_name_entry.delete(0, "end")
            self.add_quantity_entry.delete(0, "end")
            self.add_price_entry.delete(0, "end")
            self.update_inventory_view()
            self.receive_name_entry.configure(values=list(self.inventory_manager.get_inventory().keys()))
            self.sell_name_entry.configure(values=list(self.inventory_manager.get_inventory().keys()))
            self.history_name_entry.configure(values=list(self.inventory_manager.get_inventory().keys()))

    def receive_product(self):
        name = self.receive_name_entry.get().strip()
        quantity = self.receive_quantity_entry.get().strip()

        success, message = self.inventory_manager.receive_product(name, quantity, self.user)
        messagebox.showinfo("Результат", message) if success else messagebox.showerror("Помилка", message)
        if success:
            self.receive_name_entry.set("")
            self.receive_quantity_entry.delete(0, "end")
            self.update_inventory_view()

    def sell_product(self):
        name = self.sell_name_entry.get().strip()
        quantity = self.sell_quantity_entry.get().strip()

        success, message = self.inventory_manager.sell_product(name, quantity, self.user)
        messagebox.showinfo("Результат", message) if success else messagebox.showerror("Помилка", message)
        if success:
            self.sell_name_entry.set("")
            self.sell_quantity_entry.delete(0, "end")
            self.update_inventory_view()

    def add_category(self):
        category = self.category_entry.get().strip()
        success, message = self.category_manager.add_category(category)
        messagebox.showinfo("Результат", message) if success else messagebox.showerror("Помилка", message)
        if success:
            self.category_entry.delete(0, "end")
            self.update_category_list()
            self.add_category_combo.configure(values=self.inventory_manager.get_categories())

    def remove_category(self):
        category = self.category_entry.get().strip()
        success, message = self.category_manager.remove_category(category)
        messagebox.showinfo("Результат", message) if success else messagebox.showerror("Помилка", message)
        if success:
            self.category_entry.delete(0, "end")
            self.update_category_list()
            self.add_category_combo.configure(values=self.inventory_manager.get_categories())

    def update_category_list(self):
        for widget in self.category_list.winfo_children():
            widget.destroy()
        for i, category in enumerate(self.category_manager.get_categories()):
            ctk.CTkLabel(self.category_list, text=category, font=FONT).grid(row=i, column=0, padx=5, pady=2)

    def update_inventory_view(self):
        for widget in self.inventory_tree.winfo_children():
            widget.destroy()

        tree = ctk.CTkFrame(self.inventory_tree)
        tree.grid(row=0, column=0, sticky="nsew")

        columns = ("Назва", "Кількість", "Ціна", "Категорія", "Останнє оновлення", "Статус")
        for col in columns:
            ctk.CTkLabel(tree, text=col, font=FONT).grid(row=0, column=columns.index(col), padx=5, pady=5)

        for i, (name, details) in enumerate(self.inventory_manager.get_inventory().items(), 1):
            status = "Низький залишок!" if details["low_stock_alert"] else "OK"
            ctk.CTkLabel(tree, text=name, font=FONT).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(tree, text=details["quantity"], font=FONT).grid(row=i, column=1, padx=5, pady=2)
            ctk.CTkLabel(tree, text=format_currency(details["price"]), font=FONT).grid(row=i, column=2, padx=5, pady=2)
            ctk.CTkLabel(tree, text=details["category"], font=FONT).grid(row=i, column=3, padx=5, pady=2)
            ctk.CTkLabel(tree, text=details["last_updated"], font=FONT).grid(row=i, column=4, padx=5, pady=2)
            ctk.CTkLabel(tree, text=status, font=FONT, text_color="red" if details["low_stock_alert"] else "green").grid(row=i, column=5, padx=5, pady=2)

    def update_transactions_view(self):
        for widget in self.transactions_tree.winfo_children():
            widget.destroy()

        tree = ctk.CTkFrame(self.transactions_tree)
        tree.grid(row=0, column=0, sticky="nsew")

        columns = ("Дія", "Товар", "Кількість", "Ціна", "Сума", "Час", "Користувач")
        for col in columns:
            ctk.CTkLabel(tree, text=col, font=FONT).grid(row=0, column=columns.index(col), padx=5, pady=5)

        for i, transaction in enumerate(self.inventory_manager.get_transactions(), 1):
            ctk.CTkLabel(tree, text=transaction["action"], font=FONT).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(tree, text=transaction["name"], font=FONT).grid(row=i, column=1, padx=5, pady=2)
            ctk.CTkLabel(tree, text=transaction["quantity"], font=FONT).grid(row=i, column=2, padx=5, pady=2)
            ctk.CTkLabel(tree, text=format_currency(transaction["price"]), font=FONT).grid(row=i, column=3, padx=5, pady=2)
            ctk.CTkLabel(tree, text=format_currency(transaction["total"]), font=FONT).grid(row=i, column=4, padx=5, pady=2)
            ctk.CTkLabel(tree, text=transaction["timestamp"], font=FONT).grid(row=i, column=5, padx=5, pady=2)
            ctk.CTkLabel(tree, text=transaction["user"], font=FONT).grid(row=i, column=6, padx=5, pady=2)

    def update_history_view(self):
        for widget in self.history_tree.winfo_children():
            widget.destroy()

        tree = ctk.CTkFrame(self.history_tree)
        tree.grid(row=0, column=0, sticky="nsew")

        columns = ("Зміна", "Час", "Користувач")
        for col in columns:
            ctk.CTkLabel(tree, text=col, font=FONT).grid(row=0, column=columns.index(col), padx=5, pady=5)

        name = self.history_name_entry.get().strip()
        for i, entry in enumerate(self.inventory_manager.get_history(name), 1):
            ctk.CTkLabel(tree, text=entry["change"], font=FONT).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(tree, text=entry["timestamp"], font=FONT).grid(row=i, column=1, padx=5, pady=2)
            ctk.CTkLabel(tree, text=entry["user"], font=FONT).grid(row=i, column=2, padx=5, pady=2)