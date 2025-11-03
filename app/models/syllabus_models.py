from pydantic import BaseModel
from typing import List, Dict, Optional

# data structure of output schemas
class QuestionAnswerPair(BaseModel):
    question: str
    answer: str

class ChapterQA(BaseModel):
    chapter: str
    qa_pairs: List[QuestionAnswerPair]

class VisualElement(BaseModel):
    timestamp: str
    description: str

class AnimationScript(BaseModel):
    title: str
    narration: str
    visual_elements: List[VisualElement]
    equations: List[str]
    key_timestamps: Dict[str, str]
    visual_style: str

class SyllabusItem(BaseModel):
    unit_title: str
    unit_number: str
    chapter: str
    content: List[str]
    competencies: List[str]
    explanation: str
    dependencies: Optional[List[str]] = []
    qa: ChapterQA | None = None
    animation: Optional[AnimationScript] = None

