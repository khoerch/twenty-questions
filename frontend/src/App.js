import React from 'react';
import styled from '@emotion/styled';
import QuestionInput from './components/QuestionInput';
import QuestionHistory from './components/QuestionHistory';
import SuccessModal from './components/SuccessModal';
import HintPanel from './components/HintPanel';
import Notification from './components/Notification';
import { useQuestionGame } from './hooks/useQuestionGame';

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

function App() {
  const {
    questions,
    showSuccess,
    hintsUsed,
    currentHint,
    isLoading,
    notification,
    handleNewQuestion,
    useHint,
    clearNotification
  } = useQuestionGame();

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
      
      <Notification 
        message={notification} 
        onClear={clearNotification} 
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