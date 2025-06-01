import customtkinter as ctk
from gui_components import InventoryGUI
from inventory_manager import InventoryManager
from auth_manager import AuthManager
from styles import WINDOW_TITLE, WINDOW_SIZE
from tkinter import messagebox

class InventoryApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.auth_manager = AuthManager()
        self.inventory_manager = InventoryManager()

        self.current_user = None
        self.show_login_screen()

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def show_login_screen(self):
        self.login_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.login_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.login_frame, text="Вхід у систему", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(self.login_frame, text="Логін:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.login_entry = ctk.CTkEntry(self.login_frame, width=200)
        self.login_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.login_frame, text="Пароль:", font=("Arial", 14)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ctk.CTkEntry(self.login_frame, width=200, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkButton(self.login_frame, text="Увійти", command=self.login, width=200).grid(row=3, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.login_frame, text="Зареєструватися", command=self.show_register_screen, width=200).grid(row=4, column=0, columnspan=2, pady=5)

    def show_register_screen(self):
        self.login_frame.destroy()
        self.register_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.register_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.register_frame, text="Реєстрація", font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=10)
        ctk.CTkLabel(self.register_frame, text="Логін:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.reg_login_entry = ctk.CTkEntry(self.register_frame, width=200)
        self.reg_login_entry.grid(row=1, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.register_frame, text="Пароль:", font=("Arial", 14)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.reg_password_entry = ctk.CTkEntry(self.register_frame, width=200, show="*")
        self.reg_password_entry.grid(row=2, column=1, padx=5, pady=5)

        ctk.CTkLabel(self.register_frame, text="Роль:", font=("Arial", 14)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.reg_role_combo = ctk.CTkComboBox(self.register_frame, values=["manager", "seller"], width=200)
        self.reg_role_combo.grid(row=3, column=1, padx=5, pady=5)

        ctk.CTkButton(self.register_frame, text="Зареєструватися", command=self.register, width=200).grid(row=4, column=0, columnspan=2, pady=10)
        ctk.CTkButton(self.register_frame, text="Повернутися", command=self.show_login_screen, width=200).grid(row=5, column=0, columnspan=2, pady=5)

    def login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.auth_manager.authenticate(login, password)
        if user:
            self.current_user = user
            self.login_frame.destroy()
            self.gui = InventoryGUI(self.root, self.inventory_manager, self.current_user)
        else:
            messagebox.showerror("Помилка", "Невірний логін або пароль")

    def register(self):
        login = self.reg_login_entry.get().strip()
        password = self.reg_password_entry.get().strip()
        role = self.reg_role_combo.get()
        success, message = self.auth_manager.register_user(login, password, role)
        messagebox.showinfo("Результат", message) if success else messagebox.showerror("Помилка", message)
        if success:
            self.show_login_screen()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = InventoryApp()
    app.run()