# Import aplikačního
from kivy.app import App
# Importy Kivy komponent
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
# Importy potřebných MD komponent
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
# Import databázového modulu a jeho tříd
from modules.db import Database, Oprava, Opravar, Model


# Třída se stará o vytvoření obsahu dialogového okna pro vložení nového státu do databáze
class ModelContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

# Třída vytvářející dialogové okno pro vložení nového státu
class ModelDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        # Nastavení parametrů dialogového okna
        super(ModelDialog, self).__init__(
            # Dialogové okno s uživatelským obsahem
            type="custom",
            # Vytvoření objektu s uživatelským obsahem (podle třídy StateContent)
            content_cls=ModelContent(),
            title='Nový model',
            size_hint=(.8, 1),
            # Vytvoření tlačítek s odkazy na ohlasové metody
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    # Implementace ohlasových metod
    # Uložení nového záznamu státu
    def save_dialog(self, *args):
        # Vytvoření nového datového objektu státu
        model = Model()
        # Uložení údajů o novém státu podle prvků dialogového okna
        model.znacka = self.content_cls.ids.model_short_name.text
        model.nazev = self.content_cls.ids.model_full_name.text
        # Vytvoření nového státu v databázi
        app.persons.database.create_state(model)
        # Zavření dialogového okna
        self.dismiss()

    # Zavření dialogového okna bez uložení
    def cancel_dialog(self, *args):
        self.dismiss()


# Třída se stará o vytvoření obsahu dialogového okna pro vytvoření / editaci osob
class OpravarContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)
        # Jestliže již existuje id osoby (předané jako parametr)
        if id:
            # Do proměnné person se načtou údaje z daného databázového objektu (vybrán podle id)
            # Funkce vars zajistí konverzi objektu do podoby slovníku v Pythonu (typ dictionary)
            opravar = vars(app.opravy.database.read_by_id(id))
        else:
            # Když id neexistuje, do proměnné person se vloží výchozí hodnoty (nový záznam)
            opravar = {"id":"", "jmeno":"", "zamereni": "", "vyplata": ""}

        # Do editačního prvku označeného id=person_name se předá údaj z proměnné person (jméno osoby)
        self.ids.opravar.jmeno.text = opravar['jmeno']
        # Do promměnné states budou načteny všechny státy uložené v databázi
        modely = app.opravy.database.read_modely()
        # Do promměnné menu_items se pomocí proměnné states vytvoří seznam (list) položek-států, které budou použity jako obsah DropDownMenu
        # Atribut on_release definuje metodu, která ošetří výběr některého státu
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{model.znacka}", "on_release": lambda x=f"{model.znacka}": self.set_item(x)} for model in modely]
        # Vytvoření objektu menu_states pro výběr státu
        self.menu_modely = MDDropdownMenu(
            caller=self.ids.model_item,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        # Nastavení aktivní položky v seznamu států podle státní příslušnosti dané osoby
        self.ids.model_item.set_item(opravar['zamereni'])
        self.ids.model_item.text = opravar['zamereni']

    # Metoda ošetřuje výběr státu z menu
    def set_item(self, text_item):
        # Podle textu vybrané položky se nastaví aktuálně vybraný stát
        self.ids.model_item.set_item(text_item)
        self.ids.model_item.text = text_item
        # Uzavření menu
        self.menu_modely.dismiss()


# Třída umožní vytvořit dialogové okno k editaci osobních údajů
class OpravarDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(OpravarDialog, self).__init__(
            # Vytvoření objektu s uživatelským obsahem (podle třídy PersonContent)
            type="custom",
            content_cls=OpravarContent(id=id),
            title='Záznam osoby',
            text='Ahoj',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    # Ošetření tlačítka "Uložit"
    def save_dialog(self, *args):
        # Vytvoření nového slovníku, kterému jsou předány údaje z dialogových prvků
        opravar = {}
        opravar['jmeno'] = self.content_cls.ids.opravar_jmeno.text
        opravar['zamereni'] = self.content_cls.ids.model_item.text
        # Jestliže už existuje id, provádíme aktualizaci...
        if self.id:
            opravar["id"] = self.id
            app.opravy.database.update_opravar(opravar)
        # ...v opačném případě vytváříme nový záznam
        else:
             app.opravy.database.create_opravy(opravar)
        # Zavření dialogového okna
        self.dismiss()

    # Ošetření tlačítka "Zrušit"
    def cancel_dialog(self, *args):
        self.dismiss()


# Třída MyItem řeší akce související s jednou položkou (osobou) v seznamu
class MyItem(TwoLineAvatarIconListItem):
    # Konstruktoru se předává parametr item - datový objekt jedné osoby
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        # Předání informací o osobě do parametrů widgetu
        self.id = item['id']
        self.text = item['jmeno']
        self.secondary_text = item['zamereni']
        self._no_ripple_effect = True
        # Zobrazení vlajky podle státu osoby
        self.image = ImageLeftWidget()
        # Vlajky jsou umístěny ve složce images
        self.image.source = f"images/{item['jmeno']}.png"
        self.add_widget(self.image)
        # Vložení ikony pro vymazání osoby ze seznamu
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        """
        Metoda je vyvolána po stisknutí tlačítka v oblasti widgetu
        Otevře se dialogové okno pro editaci osobních dat
        """
        self.dialog = OpravarDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        """
        Metoda je vyvolána po kliknutí na ikonu koše - vymazání záznamu
        """
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    # Reakce na stisknutí tlačítka Ano
    def yes_button_release(self, *args):
        # Vyvolána metoda zajišťující vymazání záznamu podle předaného id
        app.opravy.database.delete_opravar(self.id)
        self.dialog_confirm.dismiss()

    # Reakce na stisknutí tlačítka Ne
    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


# Třída Persons řeší akce související se seznamem osob
class Opravy(BoxLayout):
    # Metoda konstruktoru
    def __init__(self, *args, **kwargs):
        super(Opravy, self).__init__(orientation="vertical")
        # Globální proměnná - obsahuje kontext aplikace
        global app
        app = App.get_running_app()
        # Vytvoření rolovacího seznamu
        scrollview = ScrollView()
        self.list = MDList()
        # Volání metody, která vytvoří databázový objekt
        self.database = Database(dbtype='sqlite', dbname='persons.db')
        # Volání metody, která načte a přepíše seznam osob na obrazovku
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        # Vytvoření nového boxu pro tlačítka Nová osoba a Nový stát
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        # Přidání tlačítka pro vložení nové osoby
        new_opravar_btn = MDFillRoundFlatIconButton()
        new_opravar_btn.text = "Nová osoba"
        new_opravar_btn.icon = "plus"
        new_opravar_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_opravar_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_opravar_btn.md_bg_color = [0, 0.5, 0.8, 1]
        new_opravar_btn.font_style = "Button"
        new_opravar_btn.pos_hint = {"center_x": .5}
        new_opravar_btn.on_release = self.on_create_person
        button_box.add_widget(new_opravar_btn)
        # Přidání tlačítka pro vložení nového státu
        new_model_btn = MDFillRoundFlatIconButton()
        new_model_btn.text = "Nový Model"
        new_model_btn.icon = "plus"
        new_model_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_model_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_model_btn.md_bg_color = [0.8, 0.5, 0, 1]
        new_model_btn.font_style = "Button"
        new_model_btn.pos_hint = {"center_x": .6}
        new_model_btn.on_release = self.on_create_state
        button_box.add_widget(new_model_btn)
        self.add_widget(button_box)


    def rewrite_list(self):
        """
        Metoda přepíše seznam osob na obrazovce
        """
        # Odstraní všechny stávající widgety (typu MyItem) z listu
        self.list.clear_widgets()
        # Načte všechny osoby z databáze
        persons = self.database.read_all()
        # Pro všechny osoby v seznamu persons vytváří widget MyItem
        for person in persons:
            print(vars(person))
            self.list.add_widget(MyItem(item=vars(person)))

    def on_create_person(self, *args):
        """
        Metoda reaguje na tlačítko Nová osoba a vyvolá dialogové okno PersonDialog
        """
        self.dialog = PersonDialog(id=None)
        self.dialog.open()

    def on_create_state(self, *args):
        """
        Metoda reaguje na tlačítko Nový stát a vyvolá dialogové okno StateDialog
        """
        self.dialog = StateDialog()
        self.dialog.open()

    def create(self, person):
        """
        Metoda vytvoří nový záznam o osobě
        """
        create_person = Person()
        create_person.name = person['name']
        create_person.state_short = person['state_short']
        self.database.create(create_person)
        self.rewrite_list()


    def update(self, person):
        """
        Metoda aktualizuje záznam osoby
        """
        update_person = self.database.read_by_id(person['id'])
        update_person.name = person['name']
        update_person.state_short = person['state_short']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        """
        Metoda smaže záznam o osobě - podle předaného id
        """
        self.database.delete(id)
        self.rewrite_list()