import numpy as np

from bragi.constants import Constants
from bragi.components.face_recognition_model import FaceRecognitionModel


class Recognizer:
    def __init__(self, config):
        self._config = config
        self._model = FaceRecognitionModel()

    def updateOne(self, face, label):
        return self._model.update(face, label)

    def save(self):
        return self._model.save()

    def recognize(self, face):
        """
        Try to recognize face with pre-learned model. If match is found, person ID is returned.
        In other cases, zero is returned to indicate miss-match.
        :returns: int
        """
        face_id, confidence = self._model.recognize(face)
                
        if confidence < self._config.recognition.min_confidence:
            return 0

        return face_id
