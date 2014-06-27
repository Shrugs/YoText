from peewee import *
from info import *
import datetime

db = MySQLDatabase(db_name, user=db_user, passwd=db_pass, host=db_host)

class YoModel(Model):
    class Meta:
        database = db

class Yoser(YoModel):
    YoserID = PrimaryKeyField(primary_key=True, auto_increment=True)
    YoserName = CharField(100, required=True)
    PhoneNumber = CharField(10)
    Endpoint = TextField()
    Address = TextField()
    TSAdded = DateTimeField(default=datetime.datetime.now)

class Yo(YoModel):
    YoID = PrimaryKeyField(primary_key=True, auto_increment=True)
    YoFrom = ForeignKeyField(Yoser, related_name="yos_sent")
    YoTo = ForeignKeyField(Yoser, related_name="yos")
    TSAdded = DateTimeField(default=datetime.datetime.now)