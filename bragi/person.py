import os
from PIL import Image
import shutil
import uuid

from bragi.database import PersonModel
from bragi import Constants


class Person(object):
    def __init__(self, id=None):
        self.model = PersonModel.get(id=id)

        self._faces = []

    @staticmethod
    def create(first_name=None, last_name=None):
        # Create DB record
        person = PersonModel.create(first_name=first_name, last_name=last_name)

        # Create dataset directory
        os.mkdir(
            os.path.join(
                Constants.PATH_DATASET, 
                "person_{}".format(person.id)
            )
        )

        return Person(id=person.id)

    def delete(self):
        """
        Delete database record, dataset with associated faces. Model is not updated!
        """
        shutil.rmtree(self.getDatasetDirectory())

        self.model.delete()
        self._faces = []
        return None

    def getDatasetDirectory(self):
        return os.path.join(Constants.PATH_DATASET, "person_{}".format(self.model.id))

    def addRawFace(self, face, extension):
        return Image.fromarray(face).save(
            os.path.join(self.getDatasetDirectory(), "face_{}.{}".format(uuid.uuid4().hex, extension))
        )

    def addFaceFile(self, file_path):

        if not os.path.exists(self.getDatasetDirectory()):
            os.mkdir(self.getDatasetDirectory())

        shutil.move(file_path, os.path.join(self.getDatasetDirectory(), os.path.basename(file_path)))
        return True
