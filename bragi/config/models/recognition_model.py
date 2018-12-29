import pydantic

class RecognitionModel(pydantic.BaseModel):
    min_confidence: float = 50.0

    @pydantic.validator("min_confidence")
    def min_confidence_range(self, confidence):
        if 0. >= confidence or 100.0 <= confidence:
            raise ValueError("'min_confidence' is out of rance (0.0, 100.0)")
        
        return confidence