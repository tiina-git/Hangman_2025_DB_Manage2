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
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = None
        self.connect()  # Loo ühendus
        self.cursor = self.conn.cursor()
        self.read_words()


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
        self.cursor.execute("SELECT * FROM words")
        data = self.cursor.fetchall()
        return data                 # Andmed edasi view, kus for loop loeb


    """
    def add_record(self, id,word,category):
        
        if self.cursor:
            try:
                sql = f'INSERT INTO {self.table} (name, steps, quess, cheater, game_length) VALUES (?, ?, ?, ?, ?);'
                self.cursor.execute(sql, (name, steps, pc_nr, cheater, seconds))
                self.conn.commit()              # lisab tabelisee # save
                print('Mängija on lisatud tabelisse')
            except sqlite3.Error as error:
                print('Mängija lisamise tekkis tõrge: {error}') # Veateade
            finally:
                self.close_connection()
        else:
            print('Ühendus puudub, loo ühendus andmebaasiga.')
            
            
            
            def get_categories(self):
       
        self.cursor.execute("SELECT DISTINCT category FROM words")
        data = self.cursor.fetchall()
        categories = [category[0] for category in data]
        if [category[0] for category in data] == ['']:
            raise ValueError(f"Kategooria puudub.")
        categories.sort()
        categories.insert(0, 'Vali kategooria')
        print(f'Kategooriad: {categories}.')

        return [category.capitalize() for category in categories]

"""