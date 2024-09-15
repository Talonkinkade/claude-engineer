import React, { useState } from 'react';

interface TEKSStandardInputProps {
  onSubmit: (standard: string) => void;
}

const TEKSStandardInput: React.FC<TEKSStandardInputProps> = ({ onSubmit }) => {
  const [standard, setStandard] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(standard);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label htmlFor="teks-standard">TEKS Standard:</label>
      <input
        type="text"
        id="teks-standard"
        value={standard}
        onChange={(e) => setStandard(e.target.value)}
        placeholder="Enter TEKS Standard"
      />
      <button type="submit">Set Standard</button>
    </form>
  );
};

export default TEKSStandardInput;