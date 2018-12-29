import peewee

from bragi.database.connection import db

class PersonModel(peewee.Model):
    # Id is automatically created
    first_name = peewee.TextField(null=True)
    last_name = peewee.TextField(null=True)

    class Meta:
        database = db
        table_name = "people"
