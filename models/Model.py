
from models.Database import Database

class Model:
    def __init__(self):
        self.database = Database()
        self.__categories = self.database.get_categories()
        #print(f"Kategooriad, mis on tabelis olemas: {self.__categories}")

        self.database = Database()
        self.__words = self.database.read_words()
        #print(f"Sõnad{self.__words}")





    @property
    def categories(self):
        """ Taghastab kategooriate listi"""
        return self.__categories


    @property
    def get_words(self):
        return self.__words
