import React, { useState } from 'react';
import styled from '@emotion/styled';

const InputContainer = styled.form`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
`;

const Input = styled.input`
  flex: 1;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #ddd;
  border-radius: 4px;
  
  &:focus {
    outline: none;
    border-color: #666;
  }
`;

const SubmitButton = styled.button`
  padding: 12px 24px;
  background-color: #2c5282;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  
  &:disabled {
    background-color: #cbd5e0;
    cursor: not-allowed;
  }
`;

function QuestionInput({ onSubmit, disabled }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      onSubmit(question);
      setQuestion('');
    }
  };

  return (
    <InputContainer onSubmit={handleSubmit}>
      <Input
        type="text"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a yes/no question..."
        disabled={disabled}
      />
      <SubmitButton type="submit" disabled={disabled || !question.trim()}>
        Ask
      </SubmitButton>
    </InputContainer>
  );
}

export default QuestionInput; 