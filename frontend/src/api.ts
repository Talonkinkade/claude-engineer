import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust this to match your backend URL

export interface TEKSStandard {
  id: number;
  standard_code: string;
  description: string;
}

export interface Question {
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

export const api = {
  async createTEKSStandard(standardCode: string, description: string): Promise<TEKSStandard> {
    const response = await axios.post(`${API_BASE_URL}/teks_standards/`, { standard_code: standardCode, description });
    return response.data;
  },

  async getTEKSStandards(): Promise<TEKSStandard[]> {
    const response = await axios.get(`${API_BASE_URL}/teks_standards/`);
    return response.data;
  },

  async generateQuestion(teksStandardId: number, difficulty: number, questionType: string): Promise<Question> {
    const response = await axios.post(`${API_BASE_URL}/generate_question/`, {
      teks_standard_id: teksStandardId,
      difficulty,
      question_type: questionType,
    });
    return response.data;
  },

  async getSimilarQuestions(teksId: number, k: number = 5): Promise<Question[]> {
    const response = await axios.get(`${API_BASE_URL}/similar_questions/${teksId}?k=${k}`);
    return response.data;
  },
};

export default api;