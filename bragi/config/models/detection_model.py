import pydantic
import os
import enum

class DetectionOutputFormat(enum.Enum):
    PNG = "png"
    JPEG = "jpg"

    def __str__(self):
        return str(self.value)


class DetectionOutputModel(pydantic.BaseModel):
    directory: str = None
    format: DetectionOutputFormat = DetectionOutputFormat.PNG
    min_width: int = 64
    min_height: int = 64
    
    @pydantic.validator("directory")
    def directory_exists(cls, path):
        if not os.path.isdir(path):
            os.mkdir(path)
        
        return path

    @pydantic.validator("min_width")
    def min_width_range(cls, width): 
        if 0 >= width:
            raise ValueError("'min_width' is out of range (0, inf)")

        return width

    @pydantic.validator("min_height")
    def min_height_range(cls, height):
        if 0 >= height:
            raise ValueError("'min_height' out of range (0, inf)")

        return height
        

class DetectionModel(pydantic.BaseModel):
    scale_factor: float = 1.5
    min_neighbors: int = 5
    skip_frames: int = 10
    output: DetectionOutputModel = None
    classifiers: list = None

    @pydantic.validator("scale_factor")
    def scale_factor_range(cls, value):
        if value < 0.5 or value > 5:
            raise ValueError("'scale_factor' is out of range <0.5; 5>")

        return value
    
    @pydantic.validator("min_neighbors")
    def min_neighbors_range(cls, value):
        if value < 0 or value > 10:
            raise ValueError("'min_neighbors' is out of range <0, 10>")

        return value
    
    @pydantic.validator("skip_frames")
    def skip_frames_range(cls, value):
        if value < 0 or value > 25:
            raise ValueError("'skip_frames' is out of range <0, 25>")

        return value

    @pydantic.validator("classifiers")
    def classifiers_values(cls, value):
        for classifier in value:
            if not os.path.isfile(classifier):
                raise FileNotFoundError("'classifiers' contains invalid path: {}".format(classifier))
        return value
