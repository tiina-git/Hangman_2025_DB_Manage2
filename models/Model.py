
from models.Database import Database

class Model:
    def __init__(self):
        self.database = Database()
        self.__categories = self.database.get_categories()
        print(self.__categories)




    @property
    def categories(self):
        """ Taghastab kategooriate listi"""
        return self.__categories
