
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu

from modules.db import Database, Oprava, Opravar, Model


class ModelContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class ModelDialog(MDDialog):
    def __init__(self, *args, **kwargs):

        super(ModelDialog, self).__init__(

            type="custom",

            content_cls=ModelContent(),
            title='Nový model',
            size_hint=(.8, 1),

            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        model = Model()
        model.nazev = self.content_cls.ids.model_nazev.text

        app.opravy.database.create_model(model)

        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class OpravarContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class OpravarDialog(MDDialog):
    def __init__(self, *args, **kwargs):

        super(OpravarDialog, self).__init__(

            type="custom",

            content_cls=OpravarContent(),
            title='Nový opravar',
            size_hint=(.8, 1),

            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        opravar = Opravar()
        opravar.jmeno = self.content_cls.ids.opravar_jmeno.text
        app.opravy.database.create_opravar(opravar)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class OpravaContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)

        if id:
            oprava = vars(app.opravy.database.read_oprava_by_id(id))
        else:
            oprava = {"id": "", "popis": "", "opravar": "Opravář", "model": "Model"}

        self.ids.oprava_popis.text = oprava['popis']

        modely = app.opravy.database.read_modely()
        opravari = app.opravy.database.read_opravari()

        menu_items_modely = [{"viewclass": "OneLineListItem", "text": f"{model.nazev}",
                       "on_release": lambda x=f"{model.nazev}": self.set_item_model(x)} for model in modely]

        menu_items_opravari = [{"viewclass": "OneLineListItem", "text": f"{opravar.jmeno}",
                       "on_release": lambda x=f"{opravar.jmeno}": self.set_item_opravar(x)} for opravar in opravari]               

        self.menu_modely = MDDropdownMenu(
            caller=self.ids.model_item,
            items=menu_items_modely,
            position="center",
            width_mult=5,
        )

        self.menu_opravari = MDDropdownMenu(
            caller=self.ids.opravar_item,
            items=menu_items_opravari,
            position="center",
            width_mult=5,
        )

        self.ids.model_item.set_item(oprava['model'])
        self.ids.model_item.text = oprava['model']

        self.ids.opravar_item.set_item(oprava['opravar'])
        self.ids.opravar_item.text = oprava['opravar']

    def set_item_model(self, text_item):

        self.ids.model_item.set_item(text_item)
        self.ids.model_item.text = text_item

        self.menu_modely.dismiss()

    def set_item_opravar(self, text_item):

        self.ids.opravar_item.set_item(text_item)
        self.ids.opravar_item.text = text_item

        self.menu_opravari.dismiss()    


class OpravaDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(OpravaDialog, self).__init__(
            type="custom",
            content_cls=OpravaContent(id=id),
            title='Záznam opravy',
            text='Ahoj',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        oprava = {}
        oprava['popis'] = self.content_cls.ids.oprava_popis.text
        oprava['model'] = self.content_cls.ids.model_item.text
        oprava['opravar'] = self.content_cls.ids.opravar_item.text

        if self.id:
            oprava["id"] = self.id
            app.opravy.update(oprava)

        else:
            app.opravy.create(oprava)

        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()

        self.id = item['id']
        self.text = item['popis']
        self.secondary_text = item['model'] + ", " + item['opravar']
        self._no_ripple_effect = True

        self.image = ImageLeftWidget()

        self.image.source = f"images/{item['popis']}.png"
        self.add_widget(self.image)

        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        """
        Metoda je vyvolána po stisknutí tlačítka v oblasti widgetu
        Otevře se dialogové okno pro editaci osobních dat
        """
        self.dialog = OpravaDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        """
        Metoda je vyvolána po kliknutí na ikonu koše - vymazání záznamu
        """
        yes_button = MDFlatButton(
            text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu',
                                       text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.opravy.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Opravy(BoxLayout):

    def __init__(self, *args, **kwargs):
        super(Opravy, self).__init__(orientation="vertical")
        global app
        app = App.get_running_app()
        scrollview = ScrollView()
        self.list = MDList()
        self.database = Database(dbtype='sqlite', dbname='opravy.db')

        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)

        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        new_oprava_btn = MDFillRoundFlatIconButton()
        new_oprava_btn.text = "Nova oprava"
        new_oprava_btn.icon = "plus"
        new_oprava_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_oprava_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_oprava_btn.md_bg_color = [0, 0.5, 0.8, 1]
        new_oprava_btn.font_style = "Button"
        new_oprava_btn.pos_hint = {"center_x": .5}
        new_oprava_btn.on_release = self.on_create_oprava
        button_box.add_widget(new_oprava_btn)

        new_opravar_btn = MDFillRoundFlatIconButton()
        new_opravar_btn.text = "Nový opravar"
        new_opravar_btn.icon = "plus"
        new_opravar_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_opravar_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_opravar_btn.md_bg_color = [0, 0.2, 0.5, 1]
        new_opravar_btn.font_style = "Button"
        new_opravar_btn.pos_hint = {"center_x": .6}
        new_opravar_btn.on_release = self.on_create_opravar
        button_box.add_widget(new_opravar_btn)

        new_model_btn = MDFillRoundFlatIconButton()
        new_model_btn.text = "Nový Model"
        new_model_btn.icon = "plus"
        new_model_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_model_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_model_btn.md_bg_color = [0.8, 0.5, 0, 1]
        new_model_btn.font_style = "Button"
        new_model_btn.pos_hint = {"center_x": .7}
        new_model_btn.on_release = self.on_create_model
        button_box.add_widget(new_model_btn)
        self.add_widget(button_box)

    def rewrite_list(self):
        self.list.clear_widgets()
        opravy = self.database.read_opravy()

        for oprava in opravy:
            print(vars(oprava))
            self.list.add_widget(MyItem(item=vars(oprava)))

    def on_create_opravar(self, *args):
        self.dialog = OpravarDialog()
        self.dialog.open()

    def on_create_model(self, *args):
        self.dialog = ModelDialog()
        self.dialog.open()

    def on_create_oprava(self, *args):
        self.dialog = OpravaDialog(id=None)
        self.dialog.open()    

    def create(self, oprava):
        create_oprava = Oprava()
        create_oprava.popis = oprava['popis']
        create_oprava.model = oprava['model']
        create_oprava.opravar = oprava['opravar']
        self.database.create_oprava(create_oprava)
        self.rewrite_list()

    def update(self, oprava):
        update_oprava = self.database.read_oprava_by_id(oprava['id'])
        update_oprava.popis = oprava['popis']
        update_oprava.model = oprava['model']
        update_oprava.opravar = oprava['opravar']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        self.database.delete_oprava(id)
        self.rewrite_list()
