import React from 'react';
import styled from '@emotion/styled';

const ModalOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
`;

const ModalContent = styled.div`
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  text-align: center;
`;

const Title = styled.h2`
  margin-top: 0;
  color: #2c5282;
`;

const Stats = styled.div`
  margin: 20px 0;
  font-size: 18px;
`;

const HintStatus = styled.span`
  color: ${props => props.used ? '#e53e3e' : '#38a169'};
  margin-left: 5px;
`;

const CloseButton = styled.button`
  padding: 10px 20px;
  background-color: #2c5282;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
`;

function SuccessModal({ attempts, hintUsed }) {
  return (
    <ModalOverlay>
      <ModalContent>
        <Title>Congratulations!</Title>
        <p>You've guessed the correct answer!</p>
        <Stats>
          <p>Attempts: {attempts}/20</p>
          <p>
            Hint used: 
            <HintStatus used={hintUsed}>
              {hintUsed ? '✗' : '✓'}
            </HintStatus>
          </p>
        </Stats>
        <CloseButton onClick={() => window.location.reload()}>
          Play Again
        </CloseButton>
      </ModalContent>
    </ModalOverlay>
  );
}

export default SuccessModal; 