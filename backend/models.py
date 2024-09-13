from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base

import enum

class QuestionType(enum.Enum):
    multiple_choice = "multiple_choice"
    short_answer = "short_answer"
    true_false = "true_false"

class TEKSStandard(Base):
    __tablename__ = "teks_standards"

    id = Column(Integer, primary_key=True, index=True)
    standard_code = Column(String, unique=True, index=True)
    description = Column(Text)
    questions = relationship("Question", back_populates="teks_standard")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text)
    question_type = Column(Enum(QuestionType))
    difficulty = Column(Integer)
    teks_standard_id = Column(Integer, ForeignKey("teks_standards.id"))
    teks_standard = relationship("TEKSStandard", back_populates="questions")
    answer = relationship("Answer", uselist=False, back_populates="question")
    distractors = relationship("Distractor", back_populates="question")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    answer_text = Column(Text)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="answer")

class Distractor(Base):
    __tablename__ = "distractors"

    id = Column(Integer, primary_key=True, index=True)
    distractor_text = Column(Text)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="distractors")