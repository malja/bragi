import argparse
import os
import enum


class PathType(enum.Flag):
    """
    Define three path types, which might be check upon. Because PathType is Flag enum,
    values can be mixed with | operator: FILE | DIRECTORY | SYMLINK.
    """
    FILE = enum.auto()
    DIRECTORY = enum.auto()
    SYMLINK = enum.auto()

    def __str__(self):

        output = ""

        for name, member in PathType.__members__.items():
            if member.value & self.value:
                if 0 == len(output):
                    output += "{}".format(name)
                else:
                    output += " | {}".format(name)

        return output


class CheckType(enum.IntEnum):
    """
    List of all available checks for provided path.
    """
    NONE = 0
    EXISTS = 1
    DOES_NOT_EXIST = 2


class ArgumentTypePath(object):

    def __init__(self, path_type: PathType, check: CheckType):

        if not isinstance(path_type, PathType):
            raise TypeError("Parameter 'path_type' should be of type PathType.")

        if not isinstance(check, CheckType):
            raise TypeError("Parameter 'check' should be of type CheckType.")

        self._type = path_type
        self._check = check

    def __call__(self, path: str):

        # Special case. It means sys.str{in, out}
        if path == "-":
            if self._type & (PathType.DIRECTORY | PathType.SYMLINK):
                raise argparse.ArgumentTypeError("Standard input/output (-) is not allowed as directory or symlink path.")
            
            return path

        # Check normal path
        exists = os.path.exists(path)
        if  (self._check == CheckType.EXISTS and not exists) or \
            (self._check == CheckType.DOES_NOT_EXIST and exists):
            raise argparse.ArgumentTypeError("Path '{}' {} not exist.".format(path, "should" if exists else "does"))

        path_type = 0
        
        if os.path.isfile(path):
            path_type = PathType.FILE
        
        if os.path.islink(path):
            path_type = PathType.SYMLINK

        if os.path.isdir(path):
            path_type = PathType.DIRECTORY

        if not path_type & self._type:
            raise argparse.ArgumentTypeError("Path type {} does not match requirements: {}.".format(path_type, self._type))

        return path


def parse_command_line_arguments():
    """
    Parse command line arguments with argparse and return argparse.Namespace with all parsed 
    arguments.
    :returns: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="Detect and recognize faces in video files.")
    subparsers = parser.add_subparsers(title="Actions", dest="action", help="Which action should be run.")
    subparsers.required = True

    # Action = "detect"
    parser_detect = subparsers.add_parser("detect", help="Detect faces in provided video and save them into ./faces directory")
    parser_detect.add_argument("--video", dest="video", required=True, type=ArgumentTypePath(PathType.FILE, CheckType.EXISTS), 
        help="Path to input video for face recognition."
    )

    # Action = "recognize"
    parser_recognize = subparsers.add_parser("recognize", help="Recognize already known faces in provided video.")
    parser_recognize.add_argument("--video", dest="video", required=True, type=ArgumentTypePath(PathType.FILE, CheckType.EXISTS), 
        help="Path to input video for face recognition."
    )

    # Action = "dataset"
    parser_dataset = subparsers.add_parser("dataset", help="Operations with dataset.")
    subparsers_dataset = parser_dataset.add_subparsers(title="Operations", dest="operation",
        help="Which operation should be executed."
    )

    subparsers_dataset.add_parser("update", help="Attach detected faces to their owners.")
    subparsers_dataset.add_parser("train", help="Update or create model based on current dataset.")

    return parser.parse_args()