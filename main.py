import argparse

from bragi import Config
from bragi.actions import detect

parser = argparse.ArgumentParser(description="Detect and recognize faces in video files.")
parser.add_argument("action", type=str, metavar="ACTION", choices=["detect", "recognize", "dataset"], help="What action to do. 'detect' will detect new faces in video. 'recognize' recognize faces in video based on dataset. 'dataset' create dataset from detected faces.")
parser.add_argument("--video", dest="video", type=str, help="Path to input video file for detection.")
args = parser.parse_args()

config = Config.parse_file("./config.json")

if args.action == "detect":
    detect(args, config, parser)
