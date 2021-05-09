from modules.db import *

db = Database(dbtype='sqlite', username='root', password='', dbname='opravy.db')

oprava = Oprava()
oprava.popis = "Výměna displeje"
oprava.cena = 1800
oprava.model = "Apple iPhone 8"
oprava.opravar = "Bořek Opravar"
db.create_oprava(oprava)

opravar = Opravar()
opravar.jmeno = "Bořek Opravar"
opravar.vyplata = 21000
opravar.zamereni = "Apple"
db.create_opravar(opravar)

model = Model()
model.nazev = "Apple iPhone 8"
db.create_model(model)
