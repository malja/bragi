import json
import pydantic
from .models import Detection
import os

class Config(pydantic.BaseModel):
    detection: Detection = None
