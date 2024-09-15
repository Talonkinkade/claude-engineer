from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base

import enum

class QuestionType(enum.Enum):
    multiple_choice = "multiple_choice"
    short_answer = "short_answer"
    true_false = "true_false"
    drag_and_drop = "drag_and_drop"
    inline_choice = "inline_choice"

class WizardData(Base):
    __tablename__ = "wizard_data"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    grade_level = Column(String)
    num_questions = Column(Integer)
    teks_standard = Column(String)
    topic = Column(String)
    questions = relationship("Question", back_populates="wizard_data")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    wizard_id = Column(Integer, ForeignKey("wizard_data.id"))
    question_text = Column(Text)
    answer = Column(Text)
    question_type = Column(Enum(QuestionType))
    difficulty = Column(Integer)
    wizard_data = relationship("WizardData", back_populates="questions")
    distractors = relationship("Distractor", back_populates="question")

class Distractor(Base):
    __tablename__ = "distractors"

    id = Column(Integer, primary_key=True, index=True)
    distractor_text = Column(Text)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="distractors")

class TEKSStandard(Base):
    __tablename__ = "teks_standards"

    id = Column(Integer, primary_key=True, index=True)
    standard_code = Column(String, unique=True, index=True)
    description = Column(Text)