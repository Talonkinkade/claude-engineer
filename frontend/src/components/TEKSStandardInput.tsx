import React, { useState } from 'react';

interface TEKSStandardInputProps {
  onSubmit: (standardCode: string, description: string) => void;
}

const TEKSStandardInput: React.FC<TEKSStandardInputProps> = ({ onSubmit }) => {
  const [standardCode, setStandardCode] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(standardCode, description);
    setStandardCode('');
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="standardCode">TEKS Standard Code:</label>
        <input
          type="text"
          id="standardCode"
          value={standardCode}
          onChange={(e) => setStandardCode(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="description">Description:</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />
      </div>
      <button type="submit">Add TEKS Standard</button>
    </form>
  );
};

export default TEKSStandardInput;