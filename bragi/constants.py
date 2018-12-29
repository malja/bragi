import os

class Constants(object):

    PATH_DATASET = "./dataset"
    
    FILE_DATABASE = "./dataset.db"
    FILE_MODEL = "./model.xml"

    def __setattr__(self, *vars):
        raise NotImplementedError("Constants may not be changed.")
