import { useState } from 'react';
import { evaluateQuestion } from '../api/questionService';

export const useQuestionGame = () => {
  const [questions, setQuestions] = useState([]);
  const [showSuccess, setShowSuccess] = useState(false);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [currentHint, setCurrentHint] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotification] = useState('');

  const handleNewQuestion = async (question) => {
    if (questions.length >= 20) {
      return;
    }
    
    setIsLoading(true);
    try {
      const response = await evaluateQuestion(question);
      console.log("API Response:", response);
      
      if (response.is_yes_no === false || response.isYesNo === false) {
        setNotification("Please ask a yes/no question!");
        setTimeout(() => setNotification(''), 5000);
        return;
      }
      
      setQuestions([...questions, {
        question,
        response: response.answer,
        relevance: response.relevance,
        isCorrect: response.isCorrect || response.is_correct || false
      }]);
  
      if (response.isCorrect || response.is_correct) {
        setShowSuccess(true);
      }
    } catch (error) {
      setNotification("Error evaluating question. Please try again.");
      setTimeout(() => setNotification(''), 5000);
    } finally {
      setIsLoading(false);
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

  const clearNotification = () => {
    setNotification('');
  };

  return {
    questions,
    showSuccess,
    hintsUsed,
    currentHint,
    isLoading,
    notification,
    handleNewQuestion,
    useHint,
    clearNotification
  };
}; 