import argparse
import cv2
import uuid
import os
import sys
from bragi import Detector
from bragi import Config

parser = argparse.ArgumentParser(description="Detect and recognize faces in video files.")
parser.add_argument("action", type=str, metavar="ACTION", choices=["detect", "recognize", "dataset"], help="What action to do. 'detect' will detect new faces in video. 'recognize' recognize faces in video based on dataset. 'dataset' create dataset from detected faces.")
parser.add_argument("--video", dest="video", type=str, help="Path to input video file for detection.")
args = parser.parse_args()

config = Config.parse_file("./config.json")

if args.action == "detect":

    if not args.video:
        parser.print_usage()
        print("{} error: the following arguments are required: --video".format(sys.argv[0]))
        exit(1)

    try:
        with Detector(args.video, config) as detector:
            for faces in detector.detect():
                for face in faces:
                    cv2.imwrite(
                        os.path.join(
                            config.detection.output.directory,
                            "face_{}.{}".format(
                                uuid.uuid4().hex,
                                config.detection.output.format
                            )
                        ),
                        face
                    )
    except Exception as e:
        print("Error: {}".format(e))
