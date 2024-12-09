import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random

class User:
    def __init__(self, id, username, money):
        self.id = id
        self.username = username
        self.money = money

class DataBase:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                money INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    def user_signin(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1], user_data[3])
        else:
            return None

    def user_signup(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return False  # Kullanıcı adı zaten var
        money = random.randint(50, 100)
        cursor.execute("INSERT INTO users (username, password, money) VALUES (?, ?, ?)", (username, password, money))
        self.conn.commit()
        return True

    def update_user_money(self, user_id, money):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET money = ? WHERE id = ?", (money, user_id))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

db = DataBase()

def login():
    username = username_entry.get()
    password = password_entry.get()
    user = db.user_signin(username, password)
    if user:
        messagebox.showinfo("Başarılı", f"Hoş geldiniz, {username}!")
        open_dashboard(user)
    else:
        messagebox.showerror("Hata", "Kullanıcı adı veya şifre hatalı.")

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if db.user_signup(username, password):
        messagebox.showinfo("Başarılı", "Kayıt işlemi tamamlandı.")
    else:
        messagebox.showerror("Hata", "Kullanıcı adı zaten mevcut.")

def open_dashboard(user):
    def check_balance():
        messagebox.showinfo("Bakiye", f"Hesabınızda {user.money} TL var.")

    def deposit():
        amount = simpledialog.askinteger("Para Yatır", "Yatırmak istediğiniz miktarı giriniz:")
        if amount:
            user.money += amount
            db.update_user_money(user.id, user.money)
            messagebox.showinfo("Başarılı", f"{amount} TL yatırıldı.")

    def withdraw():
        amount = simpledialog.askinteger("Para Çek", "Çekmek istediğiniz miktarı giriniz:")
        if amount:
            if amount > user.money:
                messagebox.showerror("Hata", "Yetersiz bakiye.")
            else:
                user.money -= amount
                db.update_user_money(user.id, user.money)
                messagebox.showinfo("Başarılı", f"{amount} TL çekildi.")

    def transfer():
        receiver_username = simpledialog.askstring("Para Transferi", "Alıcının kullanıcı adını giriniz:")
        if receiver_username:
            cursor = db.conn.cursor()
            cursor.execute("SELECT id, money FROM users WHERE username = ?", (receiver_username,))
            receiver_data = cursor.fetchone()
            
            if receiver_data:
                receiver_id, receiver_money = receiver_data
                amount = simpledialog.askinteger("Para Transferi", "Göndermek istediğiniz miktarı giriniz:")
                if amount:
                    if amount > user.money:
                        messagebox.showerror("Hata", "Yetersiz bakiye.")
                    else:
                        user.money -= amount
                        receiver_money += amount
                        db.update_user_money(user.id, user.money)
                        db.update_user_money(receiver_id, receiver_money)
                        messagebox.showinfo("Başarılı", f"{receiver_username} kullanıcısına {amount} TL gönderildi.")
            else:
                messagebox.showerror("Hata", "Alıcı kullanıcı bulunamadı.")

    dashboard = tk.Toplevel(root)
    dashboard.title("Kullanıcı Paneli")
    dashboard.geometry("400x400")
    
    tk.Label(dashboard, text=f"Hoş geldiniz, {user.username}!", font=("Arial", 16)).pack(pady=20)
    tk.Button(dashboard, text="Bakiye Sorgula", command=check_balance, font=("Arial", 12)).pack(pady=10)
    tk.Button(dashboard, text="Para Yatır", command=deposit, font=("Arial", 12)).pack(pady=10)
    tk.Button(dashboard, text="Para Çek", command=withdraw, font=("Arial", 12)).pack(pady=10)
    tk.Button(dashboard, text="Para Transferi", command=transfer, font=("Arial", 12)).pack(pady=10)
    tk.Button(dashboard, text="Çıkış", command=dashboard.destroy, font=("Arial", 12)).pack(pady=20)

# Ana arayüz
root = tk.Tk()
root.title("Bankacılık Uygulaması")
root.geometry("500x300")

frame = tk.Frame(root)
frame.pack(pady=50)

tk.Label(frame, text="Kullanıcı Adı", font=("Arial", 14)).grid(row=0, column=0, pady=10, padx=10)
username_entry = tk.Entry(frame, font=("Arial", 14))
username_entry.grid(row=0, column=1, pady=10, padx=10)

tk.Label(frame, text="Şifre", font=("Arial", 14)).grid(row=1, column=0, pady=10, padx=10)
password_entry = tk.Entry(frame, show="*", font=("Arial", 14))
password_entry.grid(row=1, column=1, pady=10, padx=10)

tk.Button(root, text="Giriş Yap", command=login, font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Kayıt Ol", command=signup, font=("Arial", 12)).pack(pady=10)

root.mainloop()
