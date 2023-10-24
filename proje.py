import random
import json

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.money = random.randint(50, 100)

class DataBase:
    def __init__(self):
        self.file_name = 'users.json'
        self.db_data = None
        self.read_db()

    def read_db(self):
        with open(self.file_name, 'r') as json_file:
            json_data = json.load(json_file)
            self.db_data = json_data

    def transfer_money(self, sender, receiver, amount):
        if sender['money'] < amount:
            print("Yetersiz bakiye. İşlem iptal edildi.")
            return

        sender['money'] -= amount
        receiver['money'] += amount
        self.save_db()
        print(f"{sender['username']} tarafından {receiver['username']} kullanıcısına {amount} TL gönderildi.")

    def save_db(self):
        with open(self.file_name, 'w') as json_file:
            json.dump(self.db_data, json_file, indent=4)

    def user_signin(self, username, password):
        for user in self.db_data['users']:
            if user['username'] == username and user['password'] == password:
                print("Giriş başarılı. Hoş geldiniz, {}.".format(username))
                return user

        print("Kullanıcı adı veya şifre hatalı. Lütfen tekrar deneyin.")
        return None

    def user_signup(self, username, password):
        for user in self.db_data['users']:
            if user['username'] == username:
                print("Kullanıcı adı zaten var. Başka bir kullanıcı adı seçin.")
                return

        user = User(username, password)
        new_user = {
            "username": user.username,
            "password": user.password,
            "money": user.money
        }
        self.db_data['users'].append(new_user)
        self.save_db()

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
            user_data = db.user_signin(kullanici_adi, kullanici_sifre)
            if user_data is not None:
                user = User(user_data['username'], user_data['password'])
                user.money = user_data['money']
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
                        user_data['money'] += add_money
                        print("Yatırılan miktar: ", add_money)
                        print("Hesabınızda bulunan miktar", user.money)
                        db.save_db()
                        continue
                    if a == "E":
                        print("Çıkışınız başarıyla yapıldı! İyi günler dileriz...")
                        break
                    if a == "B":
                        money2 = int(input("Çekmek istediğiniz para miktarını giriniz: "))
                        print("Çekilen miktar: ", money2)
                        print("Hesabınızda kalan miktar", user.money)
                        if money2 > user.money:
                            print("Yalnızca hesabınızda olduğu kadar para çekebilirsiniz!")
                        continue

                        print("Çekilen tutar:", money2)
                        user.money -= money2
                        user_data['money'] -= money2
                        db.save_db()
                        continue
                    if a == "Z":
                        receiver_username = input("Para göndermek istediğiniz kullanıcının adını giriniz: ")
                        receiver_data = None
                        for u_data in db.db_data['users']:
                            if u_data['username'] == receiver_username:
                                receiver_data = u_data
                                break
                        if receiver_data is None:
                            print("Alıcı kullanıcı bulunamadı.")
                        else:
                            transfer_amount = int(input("Göndermek istediğiniz miktarı giriniz: "))
                            db.transfer_money(user_data, receiver_data, transfer_amount)

    elif islem1 == "K":
        kullanici_adi = input("Kullanıcı adınızı giriniz:")
        kullanici_sifre = input("Şifrenizi giriniz:")
        db.user_signup(kullanici_adi, kullanici_sifre)
    else:
        print("Geçerli işlem seçiniz...")
db.save_db