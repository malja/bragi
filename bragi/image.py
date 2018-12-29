import ntpath
import uuid
import cv2
import os
import shutil

class Image:
    def __init__(self, from_data = None, from_file=None):

        self._data = None
        self._file_name = None
        self._path = None
        self._extension = None

        self._is_from_data = True

        if from_data:
            self._data = from_data
        elif from_file:

            self._is_from_data = False

            if not os.path.isfile(from_file):
                raise FileNotFoundError("File '{}' was not found.".format(from_file))

            self._path, file_name = ntpath.split(from_file)

            if file_name:
                self._file_name, self._extension = os.path.splitext(file_name)
                self._data = cv2.imread(from_file)

        else:
            raise ValueError("One of 'from_data' or 'from_file' is required.")

    def setName(self, name: str = uuid.uuid4().hex):

        name = "face_" + name

        # Image was loaded from file
        if not self._is_from_data:
            self._move(name=name)

        self._file_name = name
        return self

    def setPath(self, path: str):
        # Image was loaded from file
        if not self._is_from_data:
            self._move(path=path)

        self._path = path
        return self

    def setExtension(self, extension: str = "png"):
        # Image was loaded from file
        if not self._is_from_data:
            self._move(extension=extension)

        self._extension = extension

    def save(self):
        if self._data and self._file_name and self._path and self._extension:
            cv2.imwrite(
                "{}.{}".format(os.path.join(self._path, self._file_name), self._extension), 
                self._data
            )
            return True
        
        return False

    def _move(self, path=None, name=None, extension=None):
        path = self._path if not path else path
        name = self._file_name if not name else name
        extension = self._extension if not extension else extension

        old_path = "{}.{}".format(
            os.path.join(self._path, self._file_name),
            self._extension
        )

        new_path = "{}.{}".format(
            os.path.join(path, name),
            extension
        )

        shutil.move(old_path, new_path)

    def __str__(self):
        destination = "memory"

        if self._path and self._file_name and self._extension:
            destination = "{}.{}".format(
                os.path.join(self._path, self._file_name),
                self._extension
            )

        return "Image {x}x{y} <{dest}>".format(
            x=len(self._data),
            y=len(self._data[0]),
            dest=destination
        )

    def toRawData(self):
        return self._data