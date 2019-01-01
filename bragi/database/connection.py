import peewee
from bragi.constants import Constants

db = peewee.SqliteDatabase(Constants.FILE_DATABASE)
