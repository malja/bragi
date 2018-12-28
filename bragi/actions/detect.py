from bragi.components import Detector
from bragi import Image


def detect(args, config):
    try:
        with Detector(args.video, config) as detector:
            for faces in detector.detect():
                for face in faces:
                    
                    image = Image(from_data=face)\
                                .setName()\
                                .setExtension(config.detection.output.format)\
                                .setPath(config.detection.output.directory)
                    
                    if not image.save():
                        print("Unable to save image: '{}'.".format(image))

    except Exception as e:
        print("Error: {}".format(e))
        return False

    return True