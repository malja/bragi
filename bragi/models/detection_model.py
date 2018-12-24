import pydantic
import os

class Detection(pydantic.BaseModel):
    scale_factor: float = 1.5
    min_neighbors: int = 5
    skip_frames: int = 10
    output: dict = None
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
    
    @pydantic.validator("output")
    def output_values(cls, value):
        if  "directory" not in value:
            raise KeyError("'directory' key is not set")

        if not isinstance(value["directory"], str):
            raise TypeError("'directory' is not a string")

        if not os.path.isdir(value["directory"]):
            os.mkdir(value["directory"])
        
        if  "format" not in value:
            raise KeyError("'format' key is not set")

        if not isinstance(value["format"], str):
            raise TypeError("'format' is not string")

        if  "min_width" not in value:
            raise KeyError("'min_width' key is not set")
            
        if not isinstance(value["min_width"], int):
            raise TypeError("'min_width' is not integer")

        if value["min_width"] <= 0:
            raise ValueError("'min_width' is out of range (0, inf)")

        if "min_height" not in value:
            raise KeyError("'min_height' key is not set")
            
        if not isinstance(value["min_height"], int):
            raise TypeError("'min_height' is not integer")

        if value["min_height"] < 0:
            raise ValueError("'min_height' out of range (0, inf)")

        return value

    @pydantic.validator("classifiers")
    def classifiers_values(cls, value):
        for classifier in value:
            if not os.path.isfile(classifier):
                raise("'classifiers' contains invalid path: {}".format(classifier))
        return value
