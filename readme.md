# Math Question Generator

This project consists of a React frontend for generating math questions and a Flask backend for serving those questions.

## Project Structure

```
.
├── react-math-app/     # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── QuestionGenerator.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
└── server/             # Flask backend
    ├── app.py
    └── requirements.txt
```

## Setup and Running the Application

### Frontend (React)

1. Navigate to the React app directory:
   ```
   cd react-math-app
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

   The React app will be available at `http://localhost:3000`.

### Backend (Flask)

1. Navigate to the server directory:
   ```
   cd server
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the Flask server:
   ```
   python app.py
   ```

   The Flask server will be running at `http://localhost:5000`.

## Using the Application

1. Open your web browser and go to `http://localhost:3000`.
2. Use the dropdown to select a math topic (Addition, Subtraction, Multiplication, or Division).
3. Adjust the difficulty level using the slider.
4. Click "Generate Question" to get a new math question.
5. Enter your answer and click "Check Answer" to see if you're correct.

## Development

- The React components are in the `react-math-app/src/components` directory.
- The main App component is in `react-math-app/src/App.js`.
- The Flask server code is in `server/app.py`.

To make changes to the frontend, edit the React files and the changes will be hot-reloaded in the browser.

To modify the backend, edit `server/app.py` and restart the Flask server to see the changes.

Enjoy learning math with the Math Question Generator!
