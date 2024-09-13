import React from 'react';

interface Question {
  id: number;
  question_text: string;
  question_type: string;
  difficulty: number;
  teks_standard_id: number;
  answer?: {
    answer_text: string;
  };
  distractors?: {
    distractor_text: string;
  }[];
}

interface QuestionListProps {
  questions: Question[];
}

const QuestionList: React.FC<QuestionListProps> = ({ questions }) => {
  return (
    <div>
      <h2>Generated Questions</h2>
      {questions.map((question) => (
        <div key={question.id} className="question-item">
          <h3>Question {question.id}</h3>
          <p><strong>Text:</strong> {question.question_text}</p>
          <p><strong>Type:</strong> {question.question_type}</p>
          <p><strong>Difficulty:</strong> {question.difficulty}</p>
          <p><strong>TEKS Standard ID:</strong> {question.teks_standard_id}</p>
          {question.answer && (
            <p><strong>Answer:</strong> {question.answer.answer_text}</p>
          )}
          {question.distractors && question.distractors.length > 0 && (
            <div>
              <strong>Distractors:</strong>
              <ul>
                {question.distractors.map((distractor, index) => (
                  <li key={index}>{distractor.distractor_text}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default QuestionList;