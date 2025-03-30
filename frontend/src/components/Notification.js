import React, { useEffect } from 'react';
import styled from '@emotion/styled';

const NotificationContainer = styled.div`
  background-color: #ffebee;
  color: #c62828;
  padding: 10px 15px;
  border-radius: 4px;
  margin-bottom: 15px;
  text-align: center;
  animation: fadeOut 5s forwards;
  
  @keyframes fadeOut {
    0% { opacity: 1; }
    70% { opacity: 1; }
    100% { opacity: 0; }
  }
`;

const Notification = ({ message, onClear }) => {
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        if (onClear) onClear();
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [message, onClear]);

  if (!message) return null;
  
  return <NotificationContainer>{message}</NotificationContainer>;
};

export default Notification; 