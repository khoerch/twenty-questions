import React from 'react';
import styled from '@emotion/styled';

const Panel = styled.div`
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
`;

const HintButton = styled.button`
  padding: 8px 16px;
  background-color: ${props => props.disabled ? '#cbd5e0' : '#4a5568'};
  color: white;
  border: none;
  border-radius: 4px;
  cursor: ${props => props.disabled ? 'not-allowed' : 'pointer'};
  margin-right: 10px;
`;

const HintText = styled.div`
  margin-top: 10px;
  font-style: italic;
`;

function HintPanel({ hintsUsed, onUseHint, currentHint }) {
  return (
    <Panel>
      <div>
        <HintButton 
          onClick={onUseHint} 
          disabled={hintsUsed >= 3}
        >
          Get Hint ({3 - hintsUsed} remaining)
        </HintButton>
      </div>
      
      {currentHint && (
        <HintText>
          Hint: {currentHint}
        </HintText>
      )}
    </Panel>
  );
}

export default HintPanel; 