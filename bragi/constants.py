import os

class Constants(object):

    PATH_DATASET = "./recognition/datasets"
    PATH_FACES = "./recognition/faces"
    
    FILE_DATABASE = "./database.db"
    FILE_MODEL = "./model.xml"
    FILE_CONFIG = "./config.json"

    def __setattr__(self, *vars):
        raise NotImplementedError("Constants may not be changed.")
