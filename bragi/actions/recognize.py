import json
import os

from bragi import Person
from bragi.components import Detector, Recognizer


def recognize(args, config):

    recognizer = Recognizer(config)
    recognized_people = {}

    try:
        with Detector(args.video, config) as detector:
            for faces in detector.detect(grayscale=True):
                for face in faces:

                    person_id = recognizer.recognize(face)

                    if person_id not in recognized_people:
                        recognized_people[person_id] = []

                    # For each person ID, append time in seconds when it was detected
                    recognized_people[person_id].append(detector.getCurrentPositionTime())
                    
    except Exception as e:
        print("Error: {}".format(e))
        return False

    # Save recognized faces into JSON metadata file
    with open(os.path.join(os.path.dirname(args.video), "metadata_{}.json".format(args.video)), "w") as outfile:
        json.dump({"people":recognized_people}, outfile)

    return True
