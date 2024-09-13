import React, { useState } from 'react';
import axios from 'axios';

const QuestionGenerator = () => {
  const [topic, setTopic] = useState('Addition');
  const [difficulty, setDifficulty] = useState(1);
  const [question, setQuestion] = useState(null);
  const [options, setOptions] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [feedback, setFeedback] = useState(null);

  const generateQuestion = async () => {
    try {
      const response = await axios.post('http://localhost:5000/generate_question', {
        topic,
        difficulty
      });
      setQuestion(response.data);
      setOptions(response.data.options || generateOptions(response.data.answer));
      setSelectedAnswer(null);
      setFeedback(null);
    } catch (error) {
      console.error('Error generating question:', error);
    }
  };

  const generateOptions = (correctAnswer) => {
    const options = [correctAnswer];
    while (options.length < 4) {
      const randomOption = Math.floor(Math.random() * (correctAnswer * 2)) + 1;
      if (!options.includes(randomOption)) {
        options.push(randomOption);
      }
    }
    return shuffleArray(options);
  };

  const shuffleArray = (array) => {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
  };

  const checkAnswer = () => {
    if (selectedAnswer === question.answer) {
      setFeedback('Correct!');
    } else {
      setFeedback(`Incorrect. The correct answer is ${question.answer}.`);
    }
  };

  return (
    <div className="App">
      <h2>Math Question Generator</h2>
      <div className="control-group">
        <label>
          Topic:
          <select value={topic} onChange={(e) => setTopic(e.target.value)}>
            <option value="Addition">Addition</option>
            <option value="Subtraction">Subtraction</option>
            <option value="Multiplication">Multiplication</option>
            <option value="Division">Division</option>
          </select>
        </label>
      </div>
      <div className="control-group">
        <label>
          Difficulty:
          <input
            type="range"
            min="1"
            max="3"
            value={difficulty}
            onChange={(e) => setDifficulty(parseInt(e.target.value))}
          />
          {difficulty}
        </label>
      </div>
      <button onClick={generateQuestion}>Generate Question</button>
      {question && (
        <div className="question-container">
          <p className="question">{question.question}</p>
          <p className="teks">Related TEKS: {question.teks}</p>
          <div className="options-container">
            {options.map((option, index) => (
              <button
                key={index}
                className={`option-button ${selectedAnswer === option ? 'selected' : ''}`}
                onClick={() => setSelectedAnswer(option)}
              >
                {option}
              </button>
            ))}
          </div>
          <button onClick={checkAnswer} disabled={selectedAnswer === null}>Check Answer</button>
          {feedback && (
            <p className={`feedback ${feedback.startsWith('Correct') ? 'correct' : 'incorrect'}`}>
              {feedback}
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default QuestionGenerator;