import random

class QuestionService:
    @staticmethod
    def generate_question(topic, difficulty):
        if topic == "Addition":
            return QuestionService.generate_addition_question(difficulty)
        elif topic == "Subtraction":
            return QuestionService.generate_subtraction_question(difficulty)
        elif topic == "Multiplication":
            return QuestionService.generate_multiplication_question(difficulty)
        elif topic == "Division":
            return QuestionService.generate_division_question(difficulty)
        else:
            raise ValueError("Invalid topic")

    @staticmethod
    def generate_addition_question(difficulty):
        if difficulty == 1:
            a, b = random.randint(1, 10), random.randint(1, 10)
        elif difficulty == 2:
            a, b = random.randint(10, 50), random.randint(10, 50)
        else:
            a, b = random.randint(50, 100), random.randint(50, 100)

        answer = a + b
        question = f"What is {a} + {b}?"
        options = [answer, answer + 1, answer - 1, answer + 2]
        random.shuffle(options)

        return {
            "question": question,
            "answer": answer,
            "options": options,
            "teks": "3.4A - Solve with fluency one-step and two-step problems involving addition and subtraction within 1,000 using strategies based on place value, properties of operations, and the relationship between addition and subtraction"
        }

    @staticmethod
    def generate_subtraction_question(difficulty):
        if difficulty == 1:
            a, b = random.randint(5, 20), random.randint(1, 5)
        elif difficulty == 2:
            a, b = random.randint(25, 100), random.randint(10, 25)
        else:
            a, b = random.randint(50, 200), random.randint(25, 50)

        answer = a - b
        question = f"What is {a} - {b}?"
        options = [answer, answer + 1, answer - 1, answer + 2]
        random.shuffle(options)

        return {
            "question": question,
            "answer": answer,
            "options": options,
            "teks": "3.4A - Solve with fluency one-step and two-step problems involving addition and subtraction within 1,000 using strategies based on place value, properties of operations, and the relationship between addition and subtraction"
        }

    @staticmethod
    def generate_multiplication_question(difficulty):
        if difficulty == 1:
            a, b = random.randint(1, 5), random.randint(1, 5)
        elif difficulty == 2:
            a, b = random.randint(2, 10), random.randint(2, 10)
        else:
            a, b = random.randint(5, 12), random.randint(5, 12)

        answer = a * b
        question = f"What is {a} × {b}?"
        options = [answer, answer + a, answer - a, answer + b]
        random.shuffle(options)

        return {
            "question": question,
            "answer": answer,
            "options": options,
            "teks": "3.4K - Solve one-step and two-step problems involving multiplication and division within 100 using strategies based on objects; pictorial models, including arrays, area models, and equal groups; properties of operations; or recall of facts"
        }

    @staticmethod
    def generate_division_question(difficulty):
        if difficulty == 1:
            b = random.randint(1, 5)
            a = b * random.randint(1, 5)
        elif difficulty == 2:
            b = random.randint(2, 10)
            a = b * random.randint(2, 10)
        else:
            b = random.randint(2, 12)
            a = b * random.randint(5, 12)

        answer = a // b
        question = f"What is {a} ÷ {b}?"
        options = [answer, answer + 1, answer - 1, answer + 2]
        random.shuffle(options)

        return {
            "question": question,
            "answer": answer,
            "options": options,
            "teks": "3.4K - Solve one-step and two-step problems involving multiplication and division within 100 using strategies based on objects; pictorial models, including arrays, area models, and equal groups; properties of operations; or recall of facts"
        }