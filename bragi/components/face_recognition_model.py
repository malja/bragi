import os
import cv2
import numpy as np

from PIL import Image
from bragi.constants import Constants
from bragi.database.models import PersonModel


class FaceRecognitionModel(object):

    def __init__(self):
        self._is_loaded = False
        self._recognizer = cv2.face.LBPHFaceRecognizer_create()

        if os.path.isfile(Constants.FILE_MODEL):
            self._recognizer.read(Constants.FILE_MODEL)
            self._is_loaded = True
        else:
            print("Model file does not exits.")

    def update(self, images, labels):
        if not self._is_loaded:
            self._is_loaded = True
            self._recognizer.train([images], np.array(labels))
        else:
            self._recognizer.update([images], np.array(labels))

        return True

    def save(self):
        return self._recognizer.write(Constants.FILE_MODEL)

    def recognize(self, face):
        if not self._is_loaded:
            return 0, 0

        return self._recognizer.predict(face)

    # TODO: Decide if this method is required after all.
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
            person_dataset_path = os.path.join(Constants.PATH_DATASET, "person_{}".format(person.id))

            if not os.path.exists(person_dataset_path):
                continue

            # List of all images for current person
            photo_files = [os.path.join(person_dataset_path, item) for item in os.listdir(person_dataset_path)]
            person.update(photos_count=len(photo_files)).execute()

            # Load all photos
            for photo_file in photo_files:
                photos.append(
                    np.array(Image.open(photo_file).convert("L"))
                )
        
                labels.append(person.id)

        face_recognizer.train(photos, np.array(labels))

        if not face_recognizer.write(Constants.FILE_MODEL):
            return False

        return True
