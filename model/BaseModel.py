from peewee import *
from config import DB_NAME
db = SqliteDatabase(DB_NAME)


class BaseModel(Model):

    class Meta:
        database = db
