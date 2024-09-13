import React, { useState } from 'react';

interface QuestionGeneratorProps {
  onGenerate: (teksStandardId: number, difficulty: number, questionType: string) => void;
}

const QuestionGenerator: React.FC<QuestionGeneratorProps> = ({ onGenerate }) => {
  const [teksStandardId, setTeksStandardId] = useState('');
  const [difficulty, setDifficulty] = useState('1');
  const [questionType, setQuestionType] = useState('multiple_choice');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate(parseInt(teksStandardId), parseInt(difficulty), questionType);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="teksStandardId">TEKS Standard ID:</label>
        <input
          type="number"
          id="teksStandardId"
          value={teksStandardId}
          onChange={(e) => setTeksStandardId(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="difficulty">Difficulty:</label>
        <select
          id="difficulty"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
        >
          <option value="1">Easy</option>
          <option value="2">Medium</option>
          <option value="3">Hard</option>
        </select>
      </div>
      <div>
        <label htmlFor="questionType">Question Type:</label>
        <select
          id="questionType"
          value={questionType}
          onChange={(e) => setQuestionType(e.target.value)}
        >
          <option value="multiple_choice">Multiple Choice</option>
          <option value="short_answer">Short Answer</option>
          <option value="true_false">True/False</option>
        </select>
      </div>
      <button type="submit">Generate Question</button>
    </form>
  );
};

export default QuestionGenerator;