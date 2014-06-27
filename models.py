from peewee import *
from info import *
import datetime

db = MySQLDatabase(db_name, user=db_user, passwd=db_pass, host=db_host)

class OCModel(Model):
    class Meta:
        database = db




class Department(OCModel):
    DeptID = PrimaryKeyField(primary_key=True, auto_increment=True)
    Dept = CharField(100)

    def jsonify(self):
        return {
            'DeptID': self.DeptID,
            'Dept': self.Dept
        }
