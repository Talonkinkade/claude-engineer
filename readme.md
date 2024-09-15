# TEKS Test Question Generation Tool

This project is an Educational Content Generator API that creates test questions based on TEKS (Texas Essential Knowledge and Skills) standards. It uses a Retrieval-Augmented Generation (RAG) system to generate and retrieve relevant questions.

## Features

- Generate various types of questions based on TEKS standards:
  - Multiple-choice questions
  - Short-answer questions
  - True/false questions
  - Drag-and-drop questions
  - Inline choice questions
- Validate generated questions against TEKS standards
- Retrieve similar questions based on TEKS descriptions
- RESTful API for easy integration with frontend applications

## Project Structure

```
.
├── backend/
│   ├── rag/
│   │   ├── generator.py
│   │   └── retriever.py
│   ├── tests/
│   │   └── test_generator.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── utils.py
├── frontend/
│   └── ...
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/teks-question-generator.git
   cd teks-question-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add the following variables:
     ```
     OPENAI_API_KEY=your_openai_api_key

     DATABASE_URL=sqlite:///./test.db

     ```

5. Run the application:
   ```
   uvicorn backend.main:app --reload
   ```

## API Endpoints

- `GET /`: Root endpoint
- `POST /teks_standards/`: Create a new TEKS standard
- `GET /teks_standards/`: Get all TEKS standards
- `GET /teks_standards/{teks_id}`: Get a specific TEKS standard
- `POST /questions/`: Create a new question
- `GET /questions/`: Get all questions
- `GET /questions/{question_id}`: Get a specific question
- `POST /generate_question/`: Generate a new question based on TEKS standard
- `GET /similar_questions/{teks_id}`: Get similar questions for a TEKS standard

## Testing

Run tests using pytest:

```
pytest backend/tests
```

## Development

### Adding New Question Types

To add a new question type:

1. Add a new method in the `Generator` class in `backend/rag/generator.py`.
2. Update the `generate_question` method to include the new question type.
3. Add corresponding test cases in `backend/tests/test_generator.py`.
4. Update the API endpoints in `backend/routes.py` if necessary.

### Improving Question Generation

To improve the quality of generated questions:

1. Refine the prompts used in the `Generator` class methods.
2. Experiment with different OpenAI models or parameters.
3. Implement additional validation checks in the `validate_question` method.

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes and write tests
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the OpenAI API for question generation. Make sure to comply with OpenAI's use-case policy and pricing when using this tool.
