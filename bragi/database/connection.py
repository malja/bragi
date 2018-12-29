import peewee
from bragi import Constants

db = peewee.SqliteDatabase(Constants.PATH_DATASET_DATABASE)
