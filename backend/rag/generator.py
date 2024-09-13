import random
from typing import List, Dict, Any
import openai

class Generator:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def generate_multiple_choice_question(self, teks_standard: str, difficulty: int) -> Dict[str, Any]:
        prompt = f"Create a multiple-choice question based on the following TEKS standard: {teks_standard}. Difficulty level: {difficulty}/5"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question = response.choices[0].text.strip()
        answer, distractors = self.generate_answer_and_distractors(question, teks_standard)
        return {
            "question": question,
            "answer": answer,
            "distractors": distractors,
            "type": "multiple_choice",
            "teks": teks_standard,
            "difficulty": difficulty
        }

    def generate_short_answer_question(self, teks_standard: str, difficulty: int) -> Dict[str, Any]:
        prompt = f"Create a short-answer question based on the following TEKS standard: {teks_standard}. Difficulty level: {difficulty}/5"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question = response.choices[0].text.strip()
        answer = self.generate_answer(question, teks_standard)
        return {
            "question": question,
            "answer": answer,
            "type": "short_answer",
            "teks": teks_standard,
            "difficulty": difficulty
        }

    def generate_true_false_question(self, teks_standard: str, difficulty: int) -> Dict[str, Any]:
        prompt = f"Create a true/false question based on the following TEKS standard: {teks_standard}. Difficulty level: {difficulty}/5"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question = response.choices[0].text.strip()
        answer = self.generate_answer(question, teks_standard)
        return {
            "question": question,
            "answer": answer,
            "type": "true_false",
            "teks": teks_standard,
            "difficulty": difficulty
        }

    def generate_answer(self, question: str, teks_standard: str) -> str:
        prompt = f"Provide a correct answer to the following question based on the TEKS standard: {teks_standard}\nQuestion: {question}\nAnswer:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
        )
        return response.choices[0].text.strip()

    def generate_answer_and_distractors(self, question: str, teks_standard: str) -> tuple:
        answer = self.generate_answer(question, teks_standard)
        prompt = f"Generate 3 incorrect but plausible answer options for the following question:\nQuestion: {question}\nCorrect Answer: {answer}\nIncorrect Options:"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        distractors = [option.strip() for option in response.choices[0].text.strip().split("\n")]
        return answer, distractors

    def validate_question(self, question: Dict[str, Any], teks_standard: str) -> bool:
        prompt = f"Validate if the following question aligns with the TEKS standard. Respond with 'Valid' or 'Invalid'.\nTEKS: {teks_standard}\nQuestion: {question['question']}\nAnswer: {question['answer']}"
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0.3,
        )
        return response.choices[0].text.strip().lower() == "valid"

    def generate_question(self, teks_standard: str, difficulty: int, question_type: str = "multiple_choice") -> Dict[str, Any]:
        if question_type == "multiple_choice":
            question = self.generate_multiple_choice_question(teks_standard, difficulty)
        elif question_type == "short_answer":
            question = self.generate_short_answer_question(teks_standard, difficulty)
        elif question_type == "true_false":
            question = self.generate_true_false_question(teks_standard, difficulty)
        else:
            raise ValueError("Invalid question type")

        if self.validate_question(question, teks_standard):
            return question
        else:
            # If the question is invalid, try generating again (you might want to limit the number of retries)
            return self.generate_question(teks_standard, difficulty, question_type)