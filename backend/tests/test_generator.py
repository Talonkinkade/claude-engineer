import unittest
from unittest.mock import patch, MagicMock
from backend.rag.generator import Generator
from backend.utils import AppException

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = Generator()

    @patch('backend.rag.generator.openai')
    def test_generate_multiple_choice_question(self, mock_openai):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="What is 2 + 2?")]
        )
        question = self.generator.generate_multiple_choice_question("Math.Grade3.Addition", 3)
        self.assertIsInstance(question, dict)
        self.assertIn('question', question)
        self.assertIn('answer', question)
        self.assertIn('distractors', question)
        self.assertEqual(question['type'], 'multiple_choice')
        self.assertEqual(question['difficulty'], 3)

    @patch('backend.rag.generator.openai')
    def test_generate_short_answer_question(self, mock_openai):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="Explain the water cycle.")]
        )
        question = self.generator.generate_short_answer_question("Science.Grade5.WaterCycle", 4)
        self.assertIsInstance(question, dict)
        self.assertIn('question', question)
        self.assertIn('answer', question)
        self.assertEqual(question['type'], 'short_answer')
        self.assertEqual(question['difficulty'], 4)

    @patch('backend.rag.generator.openai')
    def test_generate_true_false_question(self, mock_openai):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="The Earth is flat.")]
        )
        question = self.generator.generate_true_false_question("Science.Grade4.EarthShape", 2)
        self.assertIsInstance(question, dict)
        self.assertIn('question', question)
        self.assertIn('answer', question)
        self.assertEqual(question['type'], 'true_false')
        self.assertEqual(question['difficulty'], 2)

    @patch('backend.rag.generator.openai')
    def test_generate_question_set(self, mock_openai):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="Sample question")]
        )
        questions = self.generator.generate_question_set("Math.Grade3.Addition", num_questions=3)
        self.assertIsInstance(questions, list)
        self.assertEqual(len(questions), 3)
        for question in questions:
            self.assertIsInstance(question, dict)
            self.assertIn('question', question)
            self.assertIn('answer', question)
            self.assertIn('type', question)
            self.assertIn('difficulty', question)

    @patch('backend.rag.generator.openai')
    def test_validate_question(self, mock_openai):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="Valid")]
        )
        question = {
            'question': 'What is 2 + 2?',
            'answer': '4',
            'type': 'multiple_choice',
            'difficulty': 1
        }
        is_valid = self.generator.validate_question(question, "Math.Grade3.Addition")
        self.assertTrue(is_valid)

    @patch('backend.rag.generator.openai')
    def test_generate_answer(self, mock_openai):
        mock_openai.Completion.create.return_value = MagicMock(
            choices=[MagicMock(text="4")]
        )
        answer = self.generator.generate_answer("What is 2 + 2?", "Math.Grade3.Addition")
        self.assertEqual(answer, "4")

    @patch('backend.rag.generator.openai')
    def test_generate_answer_and_distractors(self, mock_openai):
        mock_openai.Completion.create.side_effect = [
            MagicMock(choices=[MagicMock(text="4")]),
            MagicMock(choices=[MagicMock(text="3\n5\n6")])
        ]
        answer, distractors = self.generator.generate_answer_and_distractors("What is 2 + 2?", "Math.Grade3.Addition")
        self.assertEqual(answer, "4")
        self.assertEqual(distractors, ["3", "5", "6"])

    @patch('backend.rag.generator.openai')
    def test_openai_api_key_not_set(self, mock_openai):
        mock_openai.api_key = None
        with self.assertRaises(AppException):
            Generator()

if __name__ == '__main__':
    unittest.main()