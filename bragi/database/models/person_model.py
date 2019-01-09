import peewee
from bragi.database.connection import db


class PersonModel(peewee.Model):
    # Id is automatically created
    first_name = peewee.TextField(null=True)
    last_name = peewee.TextField(null=True)
    photos_count = peewee.IntegerField(null=False, default=0)

    class Meta:
        database = db
        db_table = "people"
