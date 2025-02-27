from tkinter.constants import DISABLED, NORMAL, END

from models.Database import Database
from views.View import View
from tkinter.filedialog import askopenfilename

class Controller:
    def __init__(self, model, view):
        """
        Kontrolleri konstruktor
        :param model: main-is loodud mudel
        :param view:  main-is loodud view
        """
        self.model = model
        self.view = view
        self.database = Database()

        # Nuppude 'callback' seaded
        self.btn_add_callback()
        #self.btn_edit_callback()
        #self.btn_delete_callback()
        #self.btn_open_callback()

        # Rippmenüü funktsionaalsus
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.combobox_change)

    def buttons_for_game(self):
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        self.view.cmb_category['state'] = NORMAL

    def btn_new_click(self):
        #Valitud kategooria
        selected_category = self.view.cmb_category.get()

    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        print(self.view.get_combo_categories.get(), end=" => ")  # Tekst rippmenüüst => Hooned
        #print(self.view.get_combo_categories.current())         # Rippmenüü index => 1
        if self.view.get_combo_categories.current() > 0:         # Valitud kategooria on 0
            self.view.get_txt_category.delete(0, END)            # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')    # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()


    # Nupu 'callback'
    def btn_add_callback(self):
        self.view.set_btn_add_callback(self.btn_add_click)
    """
    def btn_edit_callback(self):
        self.view.set_btn_edit_callback(self.btn_edit_click)
    
    def btn_delete_callback(self):
        self.view.set_btn_delete_callback(self.btn_delete_click)
    
    def btn_open_callback(self):
        self.view.set_btn_open_callback(self.btn_open_click)
        
    
    def btn_refresh_callback(self):
        self.view.set_btn_refresh_callback(self.refresh_table) """

    # Nuppude funktsioonid
    def btn_add_click(self):
        word = self.view.get_txt_word.get()               # Tekstikasti sisestus
        txt_category = self.view.get_txt_category.get()       # Kategooria  sisestus või valik
        #old_category = self.view.get_combo_categories.current()
        old_category = self.view.get_combo_categories.get()

        if word and  txt_category:
            try:
                self.database.add_record(word, txt_category)
                print(f"Sõna ja kategooria sisestamine {word} {txt_category}")
                #self.refresh_table()
            except Exception as error:
                print(f"Viga sõna ja kategooria sisestamisel: {error}")

        elif word and old_category:
            try:

                self.database.add_record(word, old_category)
                print(f"Sõna ainult sisestamine koos olemas oleva kategooriaga: {word}, {old_category}")
                #self.refresh_table()
            except Exception as error:
                print(f"Viga sõna ainult sisestamisel: {error}")


        else:
            print(f"add click 'tühi'")


    """
    
    
    def btn_edit_click(self):
        pass
      
        selected_id = self.get_selected_id()

        if selected_id:
            word = self.view.get_txt_word.get()
            category = self.view.get_txt_category.get()
            self.database.edit_record(selected_id, word, category)
            self.refresh_table()
            
          
    def btn_delete_click(self):
        selected_id = self.get_selected_id()

        if selected_id:
            self.database.delete(selected_id)
            self.refresh_table()

    


    def btn_open_click(self):

        db_path = askopenfilename(filetypes=[("SQLite database", "*.db")])
        if db_path:
            self.database.db_name = db_path
            self.database.connect()
            self.refresh_table()

    
        # Tabeli värskendamine
        def refresh_table(self):
            data = self.database.read_words()
            self.view.update_table(data)
            print(f"Uuendan andmeid...")
    
    
    
    
    
   # Valitud rea id saamine
    def get_selected_id(self):
        selected_item = self.view.get_my_table().focus()    # Valitud rida
        if selected_item:
            selected_values= self.view.get_my_table().item(selected_item, 'values')
            if selected_values:
                print(f"Selected item{selected_item}")
                print(f"Selected values{selected_values}")
                return int(selected_values[0])              # Tagastab id

        return None                                         # Rida pole valitud, midagi ei tagastata


            """