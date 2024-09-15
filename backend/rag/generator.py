import random
from typing import List, Dict, Any
import openai
from ..config import settings
from ..utils import AppException, log_info, log_error
from .retriever import Retriever

class Generator:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        if not openai.api_key:
            log_error("OpenAI API key is not set")
            raise AppException(status_code=500, detail="OpenAI API key is not configured")
        self.retriever = Retriever()
        self.question_cache = {}

    def generate_question(self, teks_standard: str, difficulty: int, question_type: str = "multiple_choice", subject: str = "", grade_level: str = "", topic: str = "") -> Dict[str, Any]:
        cache_key = f"{teks_standard}_{difficulty}_{question_type}_{subject}_{grade_level}_{topic}"
        if cache_key in self.question_cache:
            return self.question_cache[cache_key]

        try:
            similar_questions = self.get_similar_questions(teks_standard)
            if question_type == "multiple_choice":
                question = self.generate_multiple_choice_question(teks_standard, difficulty, subject, grade_level, topic, similar_questions)
            elif question_type == "short_answer":
                question = self.generate_short_answer_question(teks_standard, difficulty, subject, grade_level, topic, similar_questions)
            elif question_type == "true_false":
                question = self.generate_true_false_question(teks_standard, difficulty, subject, grade_level, topic, similar_questions)
            elif question_type == "drag_and_drop":
                question = self.generate_drag_and_drop_question(teks_standard, difficulty, subject, grade_level, topic, similar_questions)
            elif question_type == "inline_choice":
                question = self.generate_inline_choice_question(teks_standard, difficulty, subject, grade_level, topic, similar_questions)
            else:
                raise ValueError("Invalid question type")

            if self.validate_question(question, teks_standard):
                self.question_cache[cache_key] = question
                self.update_rag_index(question, teks_standard)
                return question
            else:
                # If the question is invalid, try generating again (you might want to limit the number of retries)
                return self.generate_question(teks_standard, difficulty, question_type, subject, grade_level, topic)
        except Exception as e:
            log_error(f"Error generating question: {str(e)}")
            raise AppException(status_code=500, detail="Failed to generate question")

    def get_similar_questions(self, teks_standard: str) -> List[Dict[str, Any]]:
        indices, _ = self.retriever.find_similar_questions(teks_standard)
        # Fetch the actual questions using the indices (you'll need to implement this part)
        return [self.get_question_by_index(idx) for idx in indices]

    def get_question_by_index(self, index: int) -> Dict[str, Any]:
        # Implement this method to fetch a question from your database using the FAISS index
        # This is a placeholder implementation
        return {"question": f"Placeholder question for index {index}"}

    def generate_multiple_choice_question(self, teks_standard: str, difficulty: int, subject: str, grade_level: str, topic: str, similar_questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            context = self.format_similar_questions(similar_questions)
            prompt = f"Create a multiple-choice question based on the following TEKS standard: {teks_standard}. Difficulty level: {difficulty}/5. Subject: {subject}. Grade level: {grade_level}. Topic: {topic}. Include 4 answer choices. Use the following similar questions as context:\n{context}"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.7,
            )
            question_text = response.choices[0].text.strip()
            answer, distractors = self.generate_answer_and_distractors(question_text, teks_standard)
            log_info(f"Generated multiple-choice question for TEKS: {teks_standard}")
            return {
                "question": question_text,
                "answer": answer,
                "distractors": distractors,
                "type": "multiple_choice",
                "teks": teks_standard,
                "difficulty": difficulty,
                "subject": subject,
                "grade_level": grade_level,
                "topic": topic
            }
        except Exception as e:
            log_error(f"Error generating multiple-choice question: {str(e)}")
            raise AppException(status_code=500, detail="Failed to generate multiple-choice question")

    def format_similar_questions(self, similar_questions: List[Dict[str, Any]]) -> str:
        return "\n".join([f"- {q['question']}" for q in similar_questions])

    # Implement similar modifications for other question type generation methods

    def validate_question(self, question: Dict[str, Any], teks_standard: str) -> bool:
        try:
            prompt = f"Validate if the following question aligns with the TEKS standard. Respond with 'Valid' or 'Invalid'.\nTEKS: {teks_standard}\nQuestion: {question['question']}\nAnswer: {question.get('answer', '')}"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=10,
                n=1,
                stop=None,
                temperature=0.3,
            )
            return response.choices[0].text.strip().lower() == "valid"
        except Exception as e:
            log_error(f"Error validating question: {str(e)}")
            raise AppException(status_code=500, detail="Failed to validate question")

    def update_rag_index(self, question: Dict[str, Any], teks_standard: str):
        # Implement this method to update the FAISS index with the new question
        question_id = self.save_question_to_database(question)  # You'll need to implement this method
        self.retriever.add_to_index(teks_standard, question_id)

    def save_question_to_database(self, question: Dict[str, Any]) -> int:
        # Implement this method to save the question to your database and return its ID
        # This is a placeholder implementation
        return random.randint(1, 1000000)

    def generate_question_set(self, teks_standard: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        question_types = ["multiple_choice", "short_answer", "true_false", "drag_and_drop", "inline_choice"]
        questions = []
        for _ in range(num_questions):
            difficulty = random.randint(1, 5)
            question_type = random.choice(question_types)
            question = self.generate_question(teks_standard, difficulty, question_type)
            questions.append(question)
        return questions

# Implement other methods (generate_short_answer_question, generate_true_false_question, etc.) with similar modifications