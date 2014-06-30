from peewee import *
from info import *
import datetime

db = MySQLDatabase(db_name, user=db_user, passwd=db_pass, host=db_host)


class YoModel(Model):
    class Meta:
        database = db


class Yoser(YoModel):
    name = CharField(100, null=False, unique=True)
    phone_number = CharField(12)
    ts_added = DateTimeField(default=datetime.datetime.now)
