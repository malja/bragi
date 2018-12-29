import argparse

from bragi import Config
from bragi.actions import detect, recognize
from bragi.argparse_helpers import CheckType, ArgumentTypePath, PathType

parser = argparse.ArgumentParser(description="Detect and recognize faces in video files.")
subparsers = parser.add_subparsers(title="Actions", dest="action", help="Which action should be run.")
subparsers.required = True

parser_detect = subparsers.add_parser("detect", help="Detect faces in provided video and save them into ./faces directory")
parser_detect.add_argument("--video", dest="video", required=True, type=ArgumentTypePath(PathType.FILE, CheckType.EXISTS), help="Path to input video for face recognition.")

parser_recognize = subparsers.add_parser("recognize", help="Recognize already known faces in provided video.")
parser_recognize.add_argument("--video", dest="video", required=True, type=ArgumentTypePath(PathType.FILE, CheckType.EXISTS), help="Path to input video for face recognition.")

parser_dataset = subparsers.add_parser("dataset", help="Operations with dataset.")
subparsers_dataset = parser_dataset.add_subparsers(title="Operations", dest="operation", help="Which operation should be executed.")

subparsers_dataset.add_parser("update", help="Attach detected faces to their owners.")
subparsers_dataset.add_parser("train", help="Update or create model based on current dataset.")

args = parser.parse_args()

config = Config.parse_file("./config.json")

return_status = True

if args.action == "detect":
    return_status = detect(args, config)

elif args.action == "recognize":
    return_status = recognize(args, config)

exit(0 if return_status else 1)