import os
from peewee import *
from config import DB_NAME
# db = SqliteDatabase(DB_NAME)

# DATABASE_URL = os.environ['DATABASE_URL']
#
# db = PostgresqlDatabase(DATABASE_URL)

db = PostgresqlDatabase(
    'd6cqnvqmkvmtiu',
    user='zlagqfcpvlqifl',
    password='195761200b0745bfea42bd3db172264b0103d4103ad45aea7dead678a38df2fa',
    host='ec2-54-83-44-4.compute-1.amazonaws.com',
    port=5432
)

class BaseModel(Model):

    class Meta:
        database = db
