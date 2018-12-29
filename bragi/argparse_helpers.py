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