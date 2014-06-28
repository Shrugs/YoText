from peewee import *
from info import *
import datetime

db = MySQLDatabase(db_name, user=db_user, passwd=db_pass, host=db_host)

class YoModel(Model):
    class Meta:
        database = db

class Yoser(YoModel):
    yoser_name = CharField(100, null=False, unique=True)
    phone_number = CharField(10)
    endpoint = TextField()
    address = TextField()
    friend = ForeignKeyField('self', related_name="friends", null=True)
    ts_added = DateTimeField(default=datetime.datetime.now)

class Yo(YoModel):
    yo_from = ForeignKeyField(Yoser, related_name="yos_sent")
    yo_to = ForeignKeyField(Yoser, related_name="yos")
    ts_added = DateTimeField(default=datetime.datetime.now)