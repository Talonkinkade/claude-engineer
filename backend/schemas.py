from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class QuestionType(str, Enum):
    multiple_choice = "multiple_choice"
    short_answer = "short_answer"
    true_false = "true_false"

class TEKSStandardBase(BaseModel):
    standard_code: str
    description: str

class TEKSStandardCreate(TEKSStandardBase):
    pass

class TEKSStandard(TEKSStandardBase):
    id: int

    class Config:
        orm_mode = True

class AnswerBase(BaseModel):
    answer_text: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True

class DistractorBase(BaseModel):
    distractor_text: str

class DistractorCreate(DistractorBase):
    pass

class Distractor(DistractorBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    question_text: str
    question_type: QuestionType
    difficulty: int

class QuestionCreate(QuestionBase):
    teks_standard_id: int

class Question(QuestionBase):
    id: int
    teks_standard_id: int
    answer: Optional[Answer]
    distractors: List[Distractor] = []

    class Config:
        orm_mode = True

class QuestionGenerationRequest(BaseModel):
    teks_standard_id: int
    difficulty: int
    question_type: QuestionType