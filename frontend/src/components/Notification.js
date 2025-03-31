import React, { useEffect } from 'react';
import styled from '@emotion/styled';

const NotificationContainer = styled.div`
  background-color: ${props => {
    switch (props.type) {
      case 'INFO':
        return '#e3f2fd';
      case 'WARNING':
        return '#fff3e0';
      case 'ERROR':
      default:
        return '#ffebee';
    }
  }};
  color: ${props => {
    switch (props.type) {
      case 'INFO':
        return '#0d47a1';
      case 'WARNING':
        return '#e65100';
      case 'ERROR':
      default:
        return '#c62828';
    }
  }};
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

const Notification = ({ message, type = 'ERROR', onClear }) => {
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        if (onClear) onClear();
      }, 5000);
      
      return () => clearTimeout(timer);
    }
  }, [message, onClear]);

  if (!message) return null;
  
  return <NotificationContainer type={type}>{message}</NotificationContainer>;
};

export default Notification; 