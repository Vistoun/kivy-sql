from sqlalchemy import create_engine, Column, ForeignKey, UniqueConstraint, desc
from sqlalchemy.types import Float, String, Integer, TIMESTAMP, Enum, Text, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Global Variables

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()

class Oprava(Base):
    __tablename__ = 'opravy'

    id = Column(Integer, primary_key=True)
    popis = Column(Text)
    opravar = Column(String, ForeignKey('opravari.id'))
    time = Column(TIMESTAMP)
    model = Column(String, ForeignKey('modely.id'))
    cena = Column(Integer)


class Opravar(Base):
    __tablename__ = 'opravari'

    id = Column(Integer, primary_key=True)
    jmeno = Column(String(length=100),nullable=False)
    zamereni = Column(Enum('Apple', 'Samsung', 'Xiaomi', 'Huawei', ))
    vyplata = Column(Integer)
    fotka = Column(BLOB) 

class Model(Base):
    __tablename__ = 'modely'

    id = Column(Integer, primary_key=True)
    nazev = Column(String(30), nullable=False)


class Database:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='../places.db'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_oprava(self, oprava):
        try:
            self.session.add(oprava)
            self.session.commit()
            return True
        except:
            return False

    def create_opravar(self, opravar):
        try:
            self.session.add(opravar)
            self.session.commit()
            return True
        except:
            return False

    def create_model(self, model):
        try:
            self.session.add(model)
            self.session.commit()
            return True
        except:
            return False

    def read_opravy(self):
        try:
            result = self.session.query(Oprava).all()
            return result
        except:
            return False

    def read_oprava_by_id(self,id):
        try:
            result = self.session.query(Oprava).get(id)
            return result
        except:
            return False        

    def read_opravari(self):
        try:
            result = self.session.query(Opravar).all()
            return result
        except:
            return False

    def read_opravar_by_id(self,id):
        try:
            result = self.session.query(Opravar).get(id)
            return result
        except:
            return False

    def read_modely(self):
        try:
            result = self.session.query(Model).all()
            return result
        except:
            return False

    def read_model_by_id(self,id):
        try:
            result = self.session.query(Model).get(id)
            return result
        except:
            return False                     

    def update(self):
        try:
            self.session.commit()
            return True
        except:
            return False

    def delete_oprava(self, id):
        try:
            oprava = self.read_oprava_by_id(id)
            self.session.delete(oprava)
            self.session.commit()
            return True
        except:
            return False

    def delete_opravar(self, id):
        try:
            opravar = self.read_opravar_by_id(id)
            self.session.delete(opravar)
            self.session.commit()
            return True
        except:
            return False

    def delete_model(self, id):
        try:
            model = self.read_model_by_id(id)
            self.session.delete(model)
            self.session.commit()
            return True
        except:
            return False

db = Database(dbtype='sqlite', dbname='opravy.db')