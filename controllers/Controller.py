from tkinter.constants import DISABLED, NORMAL, END

from models.Database import Database


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

        # Nuppude callback seaded
        self.btn_edit_callback()
        self.btn_delete_callback()
        self.btn_add_callback()
        self.btn_open_callback()

        # Rippmenüü funktsionaalsus
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.combobox_change)

    def buttons_for_game(self):
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        self.view.cmb_category['state'] = NORMAL

    def btn_new_click(self):
        selected_category = self.view.cmb_category.get()

    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        # print(self.view.get_combo_categories.get(), end=" => ") # Tekst rippmenüüst => Hoonaed
        # print(self.view.get_combo_categories.current()) # Rippmenüü index => 1
        if self.view.get_combo_categories.current() > 0:  # Vali kategooria on 0
            self.view.get_txt_category.delete(0, END) # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()
        else:
            self.view.get_txt_category.config(state='normal')  # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()


    # Näite: self.view.set_btn_cancel_callback(self.btn_cancel_click)
    def btn_edit_callback(self):
        self.view.set_btn_edit_callback(self.btn_edit_callback)

    def btn_delete_callback(self):
        self.view.set_btn_delete_callback(self.btn_delete_callback)

    def btn_add_callback(self):
        self.view.set_btn_add_callback(self.btn_add_callback)

    def btn_open_callback(self):
        self.view.set_btn_open_callback(self.btn_open_callback)