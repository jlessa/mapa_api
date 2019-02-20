from peewee import *
from config import DB_NAME
# db = SqliteDatabase(DB_NAME)


db = PostgresqlDatabase(
    'qt',
    user='postgres',
    password='postgres',
    host='35.198.9.103',
    port=5432
)


class BaseModel(Model):

    class Meta:
        database = db
