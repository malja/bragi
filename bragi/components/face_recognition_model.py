import os
import cv2
import numpy as np

from bragi import Image
from bragi import Constants
from bragi.database.models import PersonModel

class FaceRecognitionModel(object):

    @staticmethod
    def load():
        """
        Load or create face recognition model.
        :returns: cv2.LBPHFaceRecognizer
        :raises: RuntimeError when training or loading of recognition model failed.
        """
        
        if not os.path.isfile(Constants.FILE_MODEL):
            if not FaceRecognitionModel.train():
                raise RuntimeError("Recognition model could not be trained.")
        
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        if not face_recognizer.load(Constants.FILE_MODEL):
            raise RuntimeError("Recognition model could not be loaded.")

        return face_recognizer
    
    @staticmethod
    def train():
        """
        Create XML file with recognition model. This can be loaded later directly into LBPHFaceRecognizer.
        :return: True is training process was finished successfully. False otherwise.
        """
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Load all saved people
        people = PersonModel.select()

        # List of face images
        photos = []
        # List of person IDs corresponding to images in photos[]
        labels = []

        for person in people:
            # List of all images for current person
            photo_files = [ 
                item for item in os.listdir(
                    os.path.join(
                        Constants.PATH_DATASET, 
                        "person_{}".format(person.id)
                    )
                )
            ]

            # Load all photos
            for photo_file in photo_files:
                photos.append(
                    Image(
                        from_file=os.path.join(
                            os.path.join(
                                Constants.PATH_DATASET, "person_{}".format(person.id), 
                                photo_file
                            )
                        )
                    ).toRawData()
                )
        
                labels.append(person.id)

        face_recognizer.train(photos, np.array(labels))

        if not face_recognizer.save(Constants.FILE_MODEL):
            return False

        return True