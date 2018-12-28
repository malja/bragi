import argparse

from bragi import Config
from bragi.actions import detect, recognize
from bragi.helpers import require_optional_arguments

parser = argparse.ArgumentParser(description="Detect and recognize faces in video files.")
parser.add_argument("action", type=str, metavar="ACTION", choices=["detect", "recognize", "dataset"], help="What action to do. 'detect' will detect new faces in video. 'recognize' recognize faces in video based on dataset. 'dataset' create dataset from detected faces.")
parser.add_argument("--video", dest="video", type=str, help="Path to input video file for detection or face recognition.")
args = parser.parse_args()

config = Config.parse_file("./config.json")

return_status = True

if args.action == "detect":
    require_optional_arguments(["video"], args, parser)
    return_status = detect(args, config)

elif args.action == "recognize":
    require_optional_arguments(["video"], args, parser)
    return_status = recognize(args, config)

else:
    print("Unknown action.")
    exit(1)

if return_status:
    exit(0)

exit(1)