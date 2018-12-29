import os
import cv2

from bragi.database import PersonModel
from bragi import Constants

class Person(object):
    def __init__(self, id=None):
        self.model = PersonModel.get(id=id)

        self._faces = []

    def loadFaces(self):
        """
        Load faces from dataset files. If some faces are already loaded, returns True and does nothing.
        If you want to update faces, create new person object.
        """
        # Update requires creating person again from ID
        if 0 != len(self._faces):
            return
    
        face_files = [ 
            item for item in os.listdir(
                os.path.join(
                    Constants.PATH_DATASET, 
                    "person_{}".format(self.model.id)
                )
            )
        ]

        self._faces = [ cv2.imread(face_file) for face_file in face_files ]

    @staticmethod
    def create(first_name = None, last_name = None):
        # Create DB record
        person_id = PersonModel.create(first_name=first_name, last_name=last_name)

        # Create dataset directory
        os.mkdir(
            os.path.join(
                Constants.PATH_DATASET, 
                "person_{}".format(person_id)
            )
        )

        return Person(id=person_id)

    def getFaces(self):
        """
        Return loaded faces of this person. Method `loadFaces` should be called before this one, to make sure
        some faces are loaded.
        """
        return self._faces