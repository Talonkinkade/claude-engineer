from pydantic import BaseModel
from typing import List, Optional

class WizardStep1(BaseModel):
    subject: str
    grade_level: str
    num_questions: int

class WizardStep1Response(BaseModel):
    id: int
    message: str

class WizardStep2(BaseModel):
    wizard_id: int
    teks_standard: str
    topic: str

class WizardStep2Response(BaseModel):
    message: str

class GenerateQuestionsRequest(BaseModel):
    wizard_id: int

class QuestionSchema(BaseModel):
    question: str
    answer: str
    type: str
    difficulty: int
    distractors: Optional[List[str]]

class GeneratedQuestionsResponse(BaseModel):
    questions: List[QuestionSchema]

class WizardData(BaseModel):
    id: int
    subject: str
    grade_level: str
    num_questions: int
    teks_standard: Optional[str]
    topic: Optional[str]

    class Config:
        orm_mode = True

class Question(BaseModel):
    id: int
    wizard_id: int
    question_text: str
    answer: str
    question_type: str
    difficulty: int

    class Config:
        orm_mode = True