from bragi.database.connection import db
from bragi.database.models import PersonModel

db.create_tables([PersonModel], safe=True)