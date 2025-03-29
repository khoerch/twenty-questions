import React, { useState } from 'react';
import styled from '@emotion/styled';
import QuestionInput from './components/QuestionInput';
import QuestionHistory from './components/QuestionHistory';
import SuccessModal from './components/SuccessModal';
import HintPanel from './components/HintPanel';

const AppContainer = styled.div`
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
`;

const Header = styled.header`
  text-align: center;
  margin-bottom: 30px;
`;

const Title = styled.h1`
  font-size: 2rem;
  color: #1a1a1a;
`;

// API base URL
const API_URL = 'http://localhost:8000';

function App() {
  const [questions, setQuestions] = useState([]);
  const [showSuccess, setShowSuccess] = useState(false);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [currentHint, setCurrentHint] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const evaluateQuestion = async (question) => {
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/questions/evaluate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to evaluate question');
      }
      
      return await response.json();
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleNewQuestion = async (question) => {
    if (questions.length >= 20) {
      return;
    }
    
    const response = await evaluateQuestion(question);
    
    setQuestions([...questions, {
      question,
      response: response.answer,
      relevance: response.relevance,
      isCorrect: response.isCorrect
    }]);

    if (response.isCorrect) {
      setShowSuccess(true);
    }
  };

  const useHint = () => {
    if (hintsUsed < 3) {
      const hints = [
        "This is your first hint!",
        "This is your second hint!",
        "This is your third and final hint!"
      ];
      setCurrentHint(hints[hintsUsed]);
      setHintsUsed(hintsUsed + 1);
    }
  };

  return (
    <AppContainer>
      <Header>
        <Title>20 Questions</Title>
      </Header>
      
      <HintPanel 
        hintsUsed={hintsUsed} 
        onUseHint={useHint} 
        currentHint={currentHint}
      />
      
      <QuestionInput 
        onSubmit={handleNewQuestion}
        disabled={questions.length >= 20 || showSuccess || isLoading}
      />
      
      <QuestionHistory questions={questions} />
      
      {showSuccess && (
        <SuccessModal 
          attempts={questions.length}
          hintsUsed={hintsUsed}
        />
      )}
    </AppContainer>
  );
}

export default App; 