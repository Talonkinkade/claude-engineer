const API_BASE_URL = 'http://localhost:8000'; // Adjust this to match your backend URL

export interface Question {
  id: number;
  text: string;
  answer: string;
  options: string[];
}

export const generateQuestion = async (teksStandardId: number, difficulty: number, questionType: string): Promise<Question> => {
  const response = await fetch(`${API_BASE_URL}/generate_question`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ teksStandardId, difficulty, questionType }),
  });

  if (!response.ok) {
    throw new Error('Failed to generate question');
  }

  return response.json();
};

export const setTEKSStandard = async (standard: string): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/set_teks_standard`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ standard }),
  });

  if (!response.ok) {
    throw new Error('Failed to set TEKS standard');
  }
};