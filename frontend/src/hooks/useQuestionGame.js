import { useState } from 'react';
import { evaluateQuestion } from '../api/questionService';
import { getTodaysHint } from '../api/solutionService';


export const useQuestionGame = () => {
  const [questions, setQuestions] = useState([]);
  const [showSuccess, setShowSuccess] = useState(false);
  const [hintUsed, setHintUsed] = useState(false);
  const [currentHint, setCurrentHint] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [notification, setNotification] = useState('');
  const [notificationType, setNotificationType] = useState('ERROR');

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
        setNotificationType('WARNING');
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
      setNotificationType('ERROR');
      setTimeout(() => setNotification(''), 5000);
    } finally {
      setIsLoading(false);
    }
  };

  const useHint = async () => {
    if (hintUsed) {
      setNotification(`Hint: ${currentHint}`);
      setNotificationType('INFO');
      return;
    }

    try {
      setIsLoading(true);
      const hintData = await getTodaysHint();
      setHintUsed(true);
      setCurrentHint(hintData.hint);
      setNotification(`Hint: ${hintData.hint}`);
      setNotificationType('INFO');
    } catch (error) {
      setNotification("Failed to fetch hint. Please try again.");
      setNotificationType('ERROR');
      console.error("Error fetching hint:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const clearNotification = () => {
    setNotification('');
    setNotificationType('ERROR');
  };

  return {
    questions,
    showSuccess,
    hintUsed,
    currentHint,
    isLoading,
    notification,
    notificationType,
    handleNewQuestion,
    useHint,
    clearNotification
  };
}; 