import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox, Treeview
import tkinter as tk
from PIL._tkinter_finder import tk

from models.Database import Database

class View(Tk):

    def __init__(self, model):
        """
        Põhi akna konstruktor
        """
        super().__init__() # Pärib kõik originaal Tk omadused: View(Tk)
        self.model = model
        self.__myTable = None
        self.__myTable = ttk.Treeview(columns=("ID", "Word", "Category"), show="headings") #lisasin prooviks
        self.__myTable.heading("ID", text="ID")
        self.__myTable.heading("Word", text="Word")
        self.__myTable.heading("Category", text="Category")


        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Põhiaken
        self.__width = 400
        self.__height = 300
        self.title('Poomismängu andmebaasi haldus')
        self.center(self, self.__width, self.__height)

        # Paneel
        self.__frame_top, self.__frame_bottom, self.__frame_right = self.create_frames()

        # Põhivorm
        self.__lbl_category, self.__txt_category, self.__lbl_word, self.__txt_word = self.create_main_form()

        # Vana kategooria valik
        self.__lbl_old_categories, self.__combo_categories = self.create_combobox()

        # Nupud
        self.__btn_add, self.__btn_edit, self.__btn_delete, self.__btn_open, self.__btn_refresh, self.__x = self.create_buttons()

       
        self.create_table()

    @staticmethod
    def center(win, w, h):
        """
        Meetod mis paigutab etteantud akna ekraani keskele vastavalt monitori suurusele
        :param win: aken mida paigutada
        :param w:   akna laius
        :param h:   akna kõrgus
        :return:    None
        """
        x = int((win.winfo_screenwidth() / 2) - (w / 2))
        y = int((win.winfo_screenheight() / 2) - (h / 2))
        win.geometry(f'{w}x{h}+{x}+{y}')

    def create_frames(self):
        """
        Loob kaks frame mis paigutatakse põhiaknale (View)
        :return:
        """
        top = Frame(self, height=50, background='lightblue')
        bottom = Frame(self, background='lightyellow')
        right = Frame(top, background='lightgray')

        # Paneme paneelid põhi aknale
        top.pack(fill=BOTH)
        bottom.pack(fill=BOTH, expand=True)
        right.grid(row=0, column=2, rowspan=2, padx=5, pady=5)

        return top, bottom, right # Tagastame loodud paneelid õiges järjekorras

    def create_main_form(self):
        """
        Loob põhi vormi kaks labelit ja kaks sisestuskasti
        :return: lbl_1, txt_1, lbl_2, txt_2
        """
        lbl_1 = Label(self.__frame_top, text='Uus kategooria:', background='lightblue', font=('Verdana', 10, 'bold'))
        txt_1 = Entry(self.__frame_top)
        txt_1.focus()
        lbl_1.grid(row=0, column=0, pady=5, sticky=EW)
        txt_1.grid(row=0, column=1, sticky=EW)

        lbl_2 = Label(self.__frame_top, text='Sõna:', background='lightblue', font=('Verdana', 10, 'bold'))
        lbl_2.grid(row=2, column=0, pady=5, sticky=EW)
        txt_2 = Entry(self.__frame_top)
        txt_2.grid(row=2, column=1, sticky=EW)

        return lbl_1, txt_1, lbl_2, txt_2

    def create_buttons(self):
        """
        Loob kolm nuppu CRUD jaoks. Antud juhul: CUD (Create, Update, Delete)
        :return: btn_1, btn_2, btn_3
        """
        btn_1 = Button(self.__frame_right, text='Lisa')         # add
        btn_2 = Button(self.__frame_right, text='Muuda')        # edit
        btn_3 = Button(self.__frame_right, text='Kustuta')      # delete
        btn_4 = Button(self.__frame_right, text='Ava')          # open
        btn_5 = Button(self.__frame_right, text='Uuenda')       # refresh
        btn_6 = Button(self.__frame_right, text='')             # x

        btn_1.grid(row=0, column=1, padx=1, sticky=EW)
        btn_2.grid(row=1, column=2, padx=1, sticky=EW)
        btn_3.grid(row=0, column=2, padx=1, sticky=EW)
        btn_4.grid(row=1, column=1, padx=1, sticky=EW)
        btn_5.grid(row=3, column=1, padx=0, sticky=EW)
        btn_6.grid(row=3, column=2, padx=0, sticky=EW)

        return btn_1, btn_2, btn_3, btn_4, btn_5, btn_6


    # Nupud callback seaded
    def set_btn_add_callback(self, callback):
        self.__btn_add.config(command=callback)

    def set_btn_edit_callback(self, callback):
        self.__btn_edit.config(command=callback)

    def set_btn_delete_callback(self, callback):
        self.__btn_delete.config(command=callback)

    def set_btn_open_callback(self, callback):
        self.__btn_open.config(command=callback)

    def set_btn_refresh_callback(self, callback):
        self.__btn_refresh.config(command=callback)

    # Rippmenüü seaded
    def create_combobox(self):
        """
        Loob ja tagastab rippmenüü labeli ja rippmenüü enda
        :return: label, combo
        """
        label = Label(self.__frame_top, text='Vana kategooria', background='lightblue', font=('Verdana', 10, 'bold'))
        label.grid(row=1, column=0, pady=5, sticky=EW)

        combo = Combobox(self.__frame_top)
        #combo['values'] = ('Vali kategooria', 'Hooned', 'Loomad') # Näidis
        combo['values'] = self.model.categories
        combo.current(0)
        combo.grid(row=1, column=1, padx=4, sticky=EW)

        return label, combo


    def create_table(self):
        """
        Loob tabeli mis näitab kirjeid (sõnu ja nende kategooriaid). Loodud ainult tabeli päise osa
        :return: None
        """
        self.__myTable = Treeview(self.__frame_bottom)

        vsb = Scrollbar(self.__frame_bottom, orient=VERTICAL, command=self.__myTable.yview)
        vsb.pack(side=RIGHT, fill=Y)
        self.__myTable.configure(yscrollcommand=vsb.set)

        self.__myTable['columns'] = ('jrk', 'id', 'word', 'category')

        self.__myTable.column('#0', width=0, stretch=NO)
        self.__myTable.column('jrk', anchor=W, width=25)
        self.__myTable.column('id', anchor=W, width=50)
        self.__myTable.column('word', anchor=W, width=100)
        self.__myTable.column('category', anchor=W, width=100)

        self.__myTable.heading('#0', text='', anchor=CENTER)
        self.__myTable.heading('jrk', text='Jrk', anchor=CENTER)
        self.__myTable.heading('id', text='ID', anchor=CENTER)
        self.__myTable.heading('word', text='Sõna', anchor=CENTER)
        self.__myTable.heading('category', text='Kategooria', anchor=CENTER)

        # (START) Siin peaks olema andmete tabelisse lisamise või uuendamise koht

        #Andmebaasi kõigi andmete vaatamaine
        db = Database()
        data = db.read_words()
        x=1
        for row in data:
            #jrk = x
            id= row[0]
            word= row[1]
            category= row[2]

            self.__myTable.insert("", "end", values=(x, id, word, category))
            x += 1

        # (LÕPP) Siin peaks olema andmete tabelisse lisamise või uuendamise koht

        self.__myTable.pack(fill=BOTH, expand=True)



    # GETTERS
    @property
    def get_combo_categories(self):
        """
        Tagastab rippmenüü objekti
        :return: Combobox
        """
        return self.__combo_categories

    @property
    def get_txt_category(self):
        """
        Tagastab uue kategooria sisestuskasti objekti
        :return: Entry objekt
        """
        return self.__txt_category

    @property
    def get_my_table(self):
        """
        Meetod on selleks et saaks tabeli objekti mujal kasutada
        :return: tagastab __myTable objekti
        """
        return self.__myTable

    @property
    def get_txt_word(self):
        """
        Tagastab sisestuskasti kuhu saab sisestada sõna
        :return: Entry objekt
        """
        return self.__txt_word

        """
        # Kategooriate rippmenüüst tehtud valiku saamine
        def get_combobox_category(self):
            print(f"Kontrollin kas kategooria tuleb... get_combobox_category: {self.combobox_category.get()}")
            return self.combobox_category.get()
        """