from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivy.lang import Builder
from modules.Opravari_ import Opravy

class DatabaseScreen(Screen):
    pass


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        builder = Builder.load_file('main.kv')
        self.opravy = Opravy()
        builder.ids.navigation.ids.tab_manager.screens[0].add_widget(self.opravy)
        return builder


Test().run()