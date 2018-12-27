import sys

from bragi import Detector
from bragi import Image


def detect(args, config, parser):

    if not args.video:
        parser.print_usage()
        print("{} error: the following arguments are required: --video".format(sys.argv[0]))
        exit(1)

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