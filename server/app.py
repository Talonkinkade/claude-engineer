from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend.database import SessionLocal, engine
from backend import models, schemas
from backend.rag.generator import Generator

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/wizard/step1", response_model=schemas.WizardStep1Response)
async def wizard_step1(data: schemas.WizardStep1, db: Session = Depends(get_db)):
    wizard_data = models.WizardData(
        subject=data.subject,
        grade_level=data.grade_level,
        num_questions=data.num_questions
    )
    db.add(wizard_data)
    db.commit()
    db.refresh(wizard_data)
    return {"id": wizard_data.id, "message": "Step 1 completed successfully"}

@app.post("/wizard/step2", response_model=schemas.WizardStep2Response)
async def wizard_step2(data: schemas.WizardStep2, db: Session = Depends(get_db)):
    wizard_data = db.query(models.WizardData).filter(models.WizardData.id == data.wizard_id).first()
    if not wizard_data:
        raise HTTPException(status_code=404, detail="Wizard data not found")
    
    wizard_data.teks_standard = data.teks_standard
    wizard_data.topic = data.topic
    db.commit()
    return {"message": "Step 2 completed successfully"}

@app.post("/generate-questions", response_model=schemas.GeneratedQuestionsResponse)
async def generate_questions(data: schemas.GenerateQuestionsRequest, db: Session = Depends(get_db)):
    wizard_data = db.query(models.WizardData).filter(models.WizardData.id == data.wizard_id).first()
    if not wizard_data:
        raise HTTPException(status_code=404, detail="Wizard data not found")

    generator = Generator()
    questions = generator.generate_question_set(
        teks_standard=wizard_data.teks_standard,
        num_questions=wizard_data.num_questions,
        subject=wizard_data.subject,
        grade_level=wizard_data.grade_level,
        topic=wizard_data.topic
    )

    # Save generated questions to the database
    for q in questions:
        question = models.Question(
            wizard_id=wizard_data.id,
            question_text=q['question'],
            answer=q['answer'],
            question_type=q['type'],
            difficulty=q['difficulty']
        )
        db.add(question)
    db.commit()

    return {"questions": questions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)