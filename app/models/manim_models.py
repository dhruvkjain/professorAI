from pydantic import BaseModel
from typing import Optional

# data structure of output schemas
class ImprovementResult(BaseModel):
    improved_code: str