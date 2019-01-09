import os
import uuid
from PIL import Image
from bragi.components import Detector
from bragi.constants import Constants


def detect(args, config):
    """
    Detect faces in video and save them in /faces directory.
    :param args: Command line arguments.
    :param config: Parsed config
    :return: Detection status.
    """

    num_of_faces = 0

    try:
        with Detector(args.video, config) as detector:
            for faces in detector.detect():
                for face in faces:
                    num_of_faces += 1

                    Image.fromarray(face).save(
                        os.path.join(Constants.PATH_FACES, "face_{}.png".format(uuid.uuid4().hex))
                    )

    except Exception as e:
        print("Error: {}".format(e))
        return False

    print("Detection done. Found {} faces.".format(num_of_faces))
    return True
