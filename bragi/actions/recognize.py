from bragi import Person
from bragi.components import Detector, Recognizer

def recognize(args, config):

    recognizer = Recognizer(config)
    if not recognizer.setup():
        print("Error: Could not initialize recognizer.")
        return False

    try: 
        with Detector(args.video, config) as detector:
            for faces in detector.detect():
                for face in faces:
                    person_id = recognizer.recognize(face)
                    # TODO: Export recognized faces into metadata_<video_name>.json
                    print("Person ID={} recognized in time={}s".format(person_id, detector.getCurrentPositionTime()))

                    
    except Exception as e:
        print("Error: {}".format(e))
        return False

    return True