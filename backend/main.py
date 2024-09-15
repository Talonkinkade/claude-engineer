from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import engine, SessionLocal
from . import models, routes, schemas
from .utils import AppException, log_info, log_error
from .rag.generator import Generator
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

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

# Include the router
app.include_router(routes.router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    log_info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    log_info(f"Response: {response.status_code}")
    return response

@app.get("/")
async def root():
    log_info("Root endpoint accessed")
    return {"message": "Welcome to the Educational Content Generator API"}

# Wizard endpoints
@app.post("/wizard/step1", response_model=schemas.WizardStep1Response)
async def wizard_step1(data: schemas.WizardStep1, db: Session = Depends(get_db)):
    try:
        # Save the step 1 data to the database
        wizard_data = models.WizardData(
            subject=data.subject,
            grade_level=data.grade_level,
            num_questions=data.num_questions
        )
        db.add(wizard_data)
        db.commit()
        db.refresh(wizard_data)
        return {"id": wizard_data.id, "message": "Step 1 completed successfully"}
    except Exception as e:
        log_error(f"Error in wizard step 1: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/wizard/step2", response_model=schemas.WizardStep2Response)
async def wizard_step2(data: schemas.WizardStep2, db: Session = Depends(get_db)):
    try:
        # Update the wizard data with step 2 information
        wizard_data = db.query(models.WizardData).filter(models.WizardData.id == data.wizard_id).first()
        if not wizard_data:
            raise HTTPException(status_code=404, detail="Wizard data not found")
        
        wizard_data.teks_standard = data.teks_standard
        wizard_data.topic = data.topic
        db.commit()
        return {"message": "Step 2 completed successfully"}
    except Exception as e:
        log_error(f"Error in wizard step 2: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/generate-questions", response_model=schemas.GeneratedQuestionsResponse)
async def generate_questions(data: schemas.GenerateQuestionsRequest, db: Session = Depends(get_db)):
    try:
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
    except Exception as e:
        log_error(f"Error generating questions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Startup event
@app.on_event("startup")
async def startup_event():
    log_info("Application started")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    log_info("Application shutting down")