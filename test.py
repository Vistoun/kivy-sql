from db import *

db = Database(dbtype='sqlite', username='root', password='', dbname='opravy.db')

oprava = Oprava()
oprava.popis = "Výměna displeje"
oprava.cena = 1800
db.create_oprava(oprava)

opravar = Opravar()
opravar.jmeno = "Bořek Opravar"
opravar.vyplata = 21000
db.create_opravar(opravar)

model = Model()
model.nazev = "Apple iPhone 8"
db.create_model(model)
