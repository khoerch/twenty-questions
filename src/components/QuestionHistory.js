import React from 'react';
import styled from '@emotion/styled';

const HistoryContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
`;

const QuestionCard = styled.div`
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: ${props => props.isCorrect ? '#c6f6d5' : 'white'};
`;

const Question = styled.p`
  margin: 0 0 8px 0;
  font-size: 14px;
`;

const Answer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Response = styled.span`
  font-weight: bold;
  color: ${props => props.answer === 'YES' ? '#2f855a' : '#c53030'};
`;

const Relevance = styled.span`
  font-size: 12px;
  color: #666;
`;

function QuestionHistory({ questions }) {
  return (
    <HistoryContainer>
      {questions.map((q, index) => (
        <QuestionCard key={index} isCorrect={q.isCorrect}>
          <Question>{q.question}</Question>
          <Answer>
            <Response answer={q.response}>{q.response}</Response>
            <Relevance>Relevance: {q.relevance}%</Relevance>
          </Answer>
        </QuestionCard>
      ))}
    </HistoryContainer>
  );
}

export default QuestionHistory; 