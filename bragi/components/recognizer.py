from bragi.components import FaceRecognitionModel 
from bragi.database import PersonModel
from bragi import Constants
from bragi import Image

class Recognizer:
    def __init__(self, config):
        self._config = config
        self._face_recognizer = None

    def setup(self):
        try:
            self._face_recognizer = FaceRecognitionModel.load()
        except RuntimeError as e:
            print(e)
            return False

        return True

    def recognize(self, face):
        """
        Try to recognize face with pre-learned model. If match is found, person ID is returned.
        In other cases, zero is returned to indicate miss-match.
        :returns: int
        """
        face_id, confidence = self._face_recognizer.predict(face)
                
        if confidence < self._config.recognition.min_confidence:
            return 0

        return face_id
