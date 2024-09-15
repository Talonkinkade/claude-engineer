import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const QuestionWizard: React.FC = () => {
  const [step, setStep] = useState(1);
  const [wizardId, setWizardId] = useState<number | null>(null);
  const [formData, setFormData] = useState({
    subject: '',
    gradeLevel: '',
    numQuestions: 5,
    teksStandard: '',
    topic: '',
  });
  const [generatedQuestions, setGeneratedQuestions] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmitStep1 = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/wizard/step1`, {
        subject: formData.subject,
        grade_level: formData.gradeLevel,
        num_questions: parseInt(formData.numQuestions.toString(), 10),
      });
      setWizardId(response.data.id);
      setStep(2);
      setError(null);
    } catch (error) {
      console.error('Error submitting step 1:', error);
      setError('Failed to submit step 1. Please try again.');
    }
  };

  const handleSubmitStep2 = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE_URL}/wizard/step2`, {
        wizard_id: wizardId,
        teks_standard: formData.teksStandard,
        topic: formData.topic,
      });
      setStep(3);
      setError(null);
    } catch (error) {
      console.error('Error submitting step 2:', error);
      setError('Failed to submit step 2. Please try again.');
    }
  };

  const handleGenerateQuestions = async () => {
    try {
      const response = await axios.post(`${API_BASE_URL}/generate-questions`, {
        wizard_id: wizardId,
      });
      setGeneratedQuestions(response.data.questions);
      setError(null);
    } catch (error) {
      console.error('Error generating questions:', error);
      setError('Failed to generate questions. Please try again.');
    }
  };

  return (
    <div>
      <h2>Question Generator Wizard</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {step === 1 && (
        <form onSubmit={handleSubmitStep1}>
          <div>
            <label htmlFor="subject">Subject:</label>
            <input
              type="text"
              id="subject"
              name="subject"
              value={formData.subject}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label htmlFor="gradeLevel">Grade Level:</label>
            <input
              type="text"
              id="gradeLevel"
              name="gradeLevel"
              value={formData.gradeLevel}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label htmlFor="numQuestions">Number of Questions:</label>
            <input
              type="number"
              id="numQuestions"
              name="numQuestions"
              value={formData.numQuestions}
              onChange={handleInputChange}
              min="1"
              max="20"
              required
            />
          </div>
          <button type="submit">Next</button>
        </form>
      )}
      {step === 2 && (
        <form onSubmit={handleSubmitStep2}>
          <div>
            <label htmlFor="teksStandard">TEKS Standard:</label>
            <input
              type="text"
              id="teksStandard"
              name="teksStandard"
              value={formData.teksStandard}
              onChange={handleInputChange}
              required
            />
          </div>
          <div>
            <label htmlFor="topic">Topic:</label>
            <input
              type="text"
              id="topic"
              name="topic"
              value={formData.topic}
              onChange={handleInputChange}
              required
            />
          </div>
          <button type="submit">Generate Questions</button>
        </form>
      )}
      {step === 3 && (
        <div>
          <h3>Generated Questions:</h3>
          {generatedQuestions.length === 0 ? (
            <button onClick={handleGenerateQuestions}>Generate Questions</button>
          ) : (
            <ul>
              {generatedQuestions.map((question, index) => (
                <li key={index}>
                  <p><strong>Question:</strong> {question.question}</p>
                  <p><strong>Answer:</strong> {question.answer}</p>
                  <p><strong>Type:</strong> {question.type}</p>
                  <p><strong>Difficulty:</strong> {question.difficulty}</p>
                  {question.distractors && (
                    <p><strong>Distractors:</strong> {question.distractors.join(', ')}</p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default QuestionWizard;