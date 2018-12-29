import pydantic

from bragi.config.models import DetectionModel, RecognitionModel

class Config(pydantic.BaseModel):
    detection: DetectionModel = None
    recognition: RecognitionModel = None
