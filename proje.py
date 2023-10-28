import random
import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.money = random.randint(50, 100)

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

    def transfer_money(self, sender, receiver_id, amount):
        cursor = self.conn.cursor()
    
    
        cursor.execute("SELECT money FROM users WHERE id = ?", (sender.id,))
        sender_money = cursor.fetchone()[0]

        if sender_money < amount:
            print("Yetersiz bakiye. İşlem iptal edildi.")
            return

        sender_money -= amount
        cursor.execute("UPDATE users SET money = ? WHERE id = ?", (sender_money, sender.id))

    
        cursor.execute("SELECT money FROM users WHERE id = ?", (receiver_id,))
        receiver_money = cursor.fetchone()[0]
        receiver_money += amount
        cursor.execute("UPDATE users SET money = ? WHERE id = ?", (receiver_money, receiver_id))

        self.conn.commit()
        print(f"{sender.username} tarafından {receiver_username} kullanıcısına {amount} TL gönderildi.")



    def user_signin(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user_data = cursor.fetchone()
        if user_data:
            user = User(user_data[1], user_data[2])
            user.id = user_data[0]
            user.money = user_data[3]
            print("Giriş başarılı. Hoş geldiniz, {}.".format(username))
            return user
        else:
            print("Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.")
            return None

    def user_signup(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print("Kullanıcı adı zaten var. Başka bir kullanıcı adı seçin.")
            return

        user = User(username, password)
        cursor.execute("INSERT INTO users (username, password, money) VALUES (?, ?, ?)", (user.username, user.password, user.money))
        self.conn.commit()
        print("Kayıt başarılı. Hoş geldiniz, {}.".format(username))

    def close_connection(self):
        self.conn.close()

db = DataBase()

while True:
    islem = input("""Giriş yapmak istiyorsanız 'G' yazınız. Kayıt olmak istiyorsanız 'K' yazınız.
Seçim:""")
    islem1 = islem.upper()
    if islem1 == "G":
        while True:
            kullanici_adi = input("Kullanıcı adınızı giriniz:")
            kullanici_sifre = input("Şifrenizi giriniz:")
            user = db.user_signin(kullanici_adi, kullanici_sifre)
            if user is not None:
                print("""Giriş yapıldı. 
            *********************************

            Q = Bakiye sorgu
            T = Para yatır 
            E = Çıkış
            B = Para çek
            Z = Para transferi

            *********************************""")
                while True:
                    islem = input("Lütfen işlemi seçiniz:")
                    a = islem.upper()
                    if a == "Q":
                        print("Hesabınızda bulunan para miktarı:", user.money)
                        continue
                    if a == "T":
                        add_money = int(input("Yatırmak istediğiniz miktarı giriniz: "))
                        user.money += add_money
                        cursor = db.conn.cursor()
                        cursor.execute("UPDATE users SET money = ? WHERE id = ?", (user.money, user.id))
                        db.conn.commit()
                        print("Yatırılan miktar: ", add_money)
                        print("Hesabınızda bulunan miktar", user.money)
                        continue
                    if a == "E":
                        db.close_connection()
                        print("Çıkışınız başarıyla yapıldı! İyi günler dileriz...")
                        exit()
                    if a == "B":
                        money2 = int(input("Çekmek istediğiniz para miktarını giriniz: "))
                        print("Çekilen miktar: ", money2)
                        print("Hesabınızda kalan miktar", user.money)
                        if money2 > user.money:
                            print("Yalnızca hesabınızda olduğu kadar para çekebilirsiniz!")
                        else:
                            user.money -= money2
                            cursor = db.conn.cursor()
                            cursor.execute("UPDATE users SET money = ? WHERE id = ?", (user.money, user.id))
                            db.conn.commit()
                            print("Çekilen tutar:", money2)
                        continue
                    if a == "Z":
                        receiver_username = input("Para göndermek istediğiniz kullanıcının adını giriniz: ")
                        cursor = db.conn.cursor()
                        cursor.execute("SELECT id FROM users WHERE username = ?", (receiver_username,))
                        receiver_id = cursor.fetchone()
    
                        if not receiver_id:
                            print("Alıcı kullanıcı bulunamadı.")
                        else:
                            receiver_id = receiver_id[0]
                            transfer_amount = int(input("Göndermek istediğiniz miktarı giriniz: "))
                            db.transfer_money(user, receiver_id, transfer_amount)


    elif islem1 == "K":
        kullanici_adi = input("Kullanıcı adınızı giriniz:")
        kullanici_sifre = input("Şifrenizi giriniz:")
        db.user_signup(kullanici_adi, kullanici_sifre)
    else:
        print("Geçerli işlem seçiniz.")