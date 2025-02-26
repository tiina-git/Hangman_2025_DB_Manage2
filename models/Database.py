import sqlite3
import os

class Database:

    db_name = 'hangman_1.db'             # TEST
    table = 'words'                  # Vajaliku tabeli nimi

    def __init__(self):
        """ Kontolli andmebaasi olemasolu """
        if not os.path.exists(self.db_name):
            raise FileNotFoundError(f"Andmebaasi '{self.db_name}' ei leitud")

        """Konstruktor"""

        # self.read_words()
        self.conn = None  # Ühendus andmebaasiga
        self.cursor = None
        self.connect()  # Loo ühendus


    def connect(self):
        """Loob ühenduse andmebaasiga"""
        try :
            if self.conn:           # Kas on andmebaasiga ühendatud?
                self.conn.close()   # Kui ühendus on lahti, siis eelmine ühendus suletakse
                print('Varasem andmebaasi ühendus suleti')

            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Uus ühendus andmebaasiga {self.db_name} loodud')
        except sqlite3.Error as error:
            print(f'Tõrge andmebaasi ühenduse loomisel:{error}')  # Veateade
            self.conn = None
            self.cursor = None

    def close_connection(self):
        """Sulgeb andmebaasi ühenduse"""
        try:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
        except sqlite3.Error as error:
            print(f'Tõrge ühenduse sulgemisel: {error}')    # Veateade


    def read_words(self):
        """Loeb andmebaasist andmed"""
        if self.cursor:
            try:
                sql = f'SELECT * FROM words ORDER BY category, word'
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                return data
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return[]
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')



    def add_record(self,word,category=None):
        """Lisab andmebaasi sõna, kategooria"""
        if self.cursor:
            try:
                print(f"Tabeli andmete sisestus: {self.table}, Values: {word}, {category}")

                sql = f'INSERT INTO {self.table} (word, category) VALUES (?, ?);'
                self.cursor.execute(sql, (word, category))
                self.conn.commit()                      # Lisab tabelisee, sama mis 'save'
                print('Sõna sisestamine... ')
            except sqlite3.Error as error:
                print('Sisestuse  lisamise tekkis tõrge: {error}') # Veateade
            finally:
                self.close_connection()  # Test kui ei sulge andmebaasi vaid pass..
        else:
            print('Ühendus puudub, loo ühendus andmebaasiga.')


    def edit_record(self,id,word,category):
        """Muudab sisestust"""
        if self.cursor:
            try:
                sql = f"UPDATE {self.table} SET word = ?, category = ? WHERE id = ?;"
                self.cursor.execute(sql,(word,category,id))
                self.conn.commit()
                print('Sisestuse  muutmine...')
            except sqlite3.Error as error:
                print(f"Viga andmete muutmisel: {error}")
            finally:
                self.close_connection()
        else:
            print('Ühendus puudub, loo ühendus andmebaasiga.')


    def delete_record(self, id, word, category):
        """Kustutab sisestuse id järgi"""
        if self.cursor:
            try:
                sql = f"DELETE from {self.table} where id = ? ;"
                self.cursor.execute(sql, (id,))
                self.conn.commit()
                print('Sisestuse  kustutamine...')
            except sqlite3.Error as error:
                print(f"Viga andmete kustutamisel: {error}")
            finally:
                self.close_connection()
        else:
            print('Ühendus puudub, loo ühendus andmebaasiga.')


    def get_categories(self):
        """Tagastab kategooriad"""
        if self.cursor:
            try:
                sql = f'SELECT DISTINCT(category) as category FROM words ORDER BY category;'
                self.cursor.execute(sql)
                data = self.cursor.fetchall()
                data.insert(0,'Vali Kategooria')
                print('Kategooria valimine...')
                return data
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return[]
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')
