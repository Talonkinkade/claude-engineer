from flask import Flask, request, jsonify
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/generate_question', methods=['POST'])
    def generate_question():
        data = request.json
        topic = data.get('topic')
        difficulty = data.get('difficulty')

        # TODO: Implement actual question generation logic
        question = f"What is 2 + 2? (Topic: {topic}, Difficulty: {difficulty})"
        answer = 4
        options = [2, 3, 4, 5]
        teks = "3.4A - Solve with fluency one-step and two-step problems involving addition and subtraction within 1,000 using strategies based on place value, properties of operations, and the relationship between addition and subtraction"

        return jsonify({
            "question": question,
            "answer": answer,
            "options": options,
            "teks": teks
        })

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)