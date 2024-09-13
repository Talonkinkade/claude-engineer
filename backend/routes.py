from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import get_db
from .rag.generator import Generator
from .rag.retriever import Retriever

router = APIRouter()

generator = Generator(api_key="your-openai-api-key")  # Replace with your actual API key
retriever = Retriever()

# TEKS Standard routes
@router.post("/teks_standards/", response_model=schemas.TEKSStandard)
def create_teks_standard(teks_standard: schemas.TEKSStandardCreate, db: Session = Depends(get_db)):
    db_teks = models.TEKSStandard(**teks_standard.dict())
    db.add(db_teks)
    db.commit()
    db.refresh(db_teks)
    return db_teks

@router.get("/teks_standards/", response_model=List[schemas.TEKSStandard])
def read_teks_standards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    teks_standards = db.query(models.TEKSStandard).offset(skip).limit(limit).all()
    return teks_standards

@router.get("/teks_standards/{teks_id}", response_model=schemas.TEKSStandard)
def read_teks_standard(teks_id: int, db: Session = Depends(get_db)):
    db_teks = db.query(models.TEKSStandard).filter(models.TEKSStandard.id == teks_id).first()
    if db_teks is None:
        raise HTTPException(status_code=404, detail="TEKS standard not found")
    return db_teks

# Question routes
@router.post("/questions/", response_model=schemas.Question)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.get("/questions/", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questions = db.query(models.Question).offset(skip).limit(limit).all()
    return questions

@router.get("/questions/{question_id}", response_model=schemas.Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question

# Question generation route
@router.post("/generate_question/", response_model=schemas.Question)
def generate_question(request: schemas.QuestionGenerationRequest, db: Session = Depends(get_db)):
    teks_standard = db.query(models.TEKSStandard).filter(models.TEKSStandard.id == request.teks_standard_id).first()
    if teks_standard is None:
        raise HTTPException(status_code=404, detail="TEKS standard not found")

    generated_question = generator.generate_question(teks_standard.description, request.difficulty, request.question_type)
    
    db_question = models.Question(
        question_text=generated_question["question"],
        question_type=generated_question["type"],
        difficulty=generated_question["difficulty"],
        teks_standard_id=teks_standard.id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    db_answer = models.Answer(answer_text=generated_question["answer"], question_id=db_question.id)
    db.add(db_answer)

    if "distractors" in generated_question:
        for distractor in generated_question["distractors"]:
            db_distractor = models.Distractor(distractor_text=distractor, question_id=db_question.id)
            db.add(db_distractor)

    db.commit()
    db.refresh(db_question)

    return db_question

# Similar questions retrieval route
@router.get("/similar_questions/{teks_id}", response_model=List[schemas.Question])
def get_similar_questions(teks_id: int, k: int = 5, db: Session = Depends(get_db)):
    teks_standard = db.query(models.TEKSStandard).filter(models.TEKSStandard.id == teks_id).first()
    if teks_standard is None:
        raise HTTPException(status_code=404, detail="TEKS standard not found")

    similar_indices, _ = retriever.find_similar_questions(teks_standard.description, k)
    similar_questions = db.query(models.Question).filter(models.Question.id.in_(similar_indices)).all()
    return similar_questions