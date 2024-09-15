import React from 'react';
import { Question } from '../api';

interface QuestionListProps {
  questions: Question[];
}

const QuestionList: React.FC<QuestionListProps> = ({ questions }) => {
  return (
    <div className="question-list">
      <h2>Generated Questions</h2>
      {questions.length === 0 ? (
        <p>No questions generated yet.</p>
      ) : (
        <ul>
          {questions.map((question, index) => (
            <li key={index}>
              <h3>Question {index + 1}</h3>
              <p>{question.text}</p>
              <h4>Options:</h4>
              <ul>
                {question.options.map((option, optionIndex) => (
                  <li key={optionIndex}>{option}</li>
                ))}
              </ul>
              <p><strong>Answer: </strong>{question.answer}</p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default QuestionList;