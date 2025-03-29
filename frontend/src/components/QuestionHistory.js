import React from 'react';
import styled from '@emotion/styled';

const HistoryContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const QuestionCard = styled.div`
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: ${props => props.isCorrect ? '#c6f6d5' : 'white'};
`;

const QuestionText = styled.p`
  margin: 0 0 12px 0;
  font-size: 14px;
  font-style: italic;
`;

const AnswerRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const QuestionCounter = styled.span`
  font-size: 12px;
  color: #666;
  font-weight: 500;
`;

const Response = styled.span`
  font-weight: bold;
  color: ${props => props.answer === 'YES' ? '#2f855a' : '#c53030'};
`;

const Relevance = styled.span`
  font-size: 16px;
`;

function QuestionHistory({ questions }) {
  // If there are no questions, don't render anything
  if (questions.length === 0) {
    return null;
  }

  // Create a reversed copy of the questions array to show newest first
  const reversedQuestions = [...questions].reverse();

  return (
    <HistoryContainer>
      {reversedQuestions.map((q, index) => {
        // Calculate the actual question number (counting from the beginning)
        const questionNumber = questions.length - index;
        
        return (
          <QuestionCard key={index} isCorrect={q.isCorrect}>
            <QuestionText>{q.question}</QuestionText>
            <AnswerRow>
              <QuestionCounter>{questionNumber} / 20</QuestionCounter>
              <Response answer={q.response}>{q.response}</Response>
              <Relevance>
                {getRelevanceEmoji(q.relevance)}
              </Relevance>
            </AnswerRow>
          </QuestionCard>
        );
      })}
    </HistoryContainer>
  );
}

// Helper function to determine which emoji to show based on relevance
function getRelevanceEmoji(relevance) {
  if (relevance < 25) {
    return '❄️'; // Ice emoji for low relevance
  } else if (relevance > 75) {
    return '🔥'; // Fire emoji for high relevance
  } else {
    return ''; // Nothing for medium relevance
  }
}

export default QuestionHistory; 