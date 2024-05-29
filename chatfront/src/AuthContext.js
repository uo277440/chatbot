import React, { createContext, useState, useEffect } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(() => {
    const savedUser = localStorage.getItem('currentUser');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [newForumMessage, setNewForumMessage] = useState(() => {
    const savedNotification = localStorage.getItem('newForumMessage');
    return savedNotification ? JSON.parse(savedNotification) : false;
  });

  useEffect(() => {
    if (currentUser) {
      localStorage.setItem('currentUser', JSON.stringify(currentUser));
    } else {
      localStorage.removeItem('currentUser');
    }
  }, [currentUser]);

  useEffect(() => {
    localStorage.setItem('newForumMessage', JSON.stringify(newForumMessage));
  }, [newForumMessage]);

  useEffect(() => {
    const fetchCurrentUser = async () => {
      try {
        const response = await axios.get('/api/user');
        setCurrentUser(response.data.user);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    };

    if (!currentUser) {
      fetchCurrentUser();
    }

    const websocket = new WebSocket('ws://localhost:8000/ws/forum/');

    websocket.onmessage = function(event) {
      
      const data = JSON.parse(event.data);
      if (data.action === 'send') {
        if (parseInt(data.user.user_id) !== parseInt(currentUser?.user_id)) {
          console.log(data.user.user_id)
          console.log(currentUser?.user_id)
          setNewForumMessage(true);
        }
      }
    };

    return () => {
      websocket.close();
    };
  }, [currentUser]);

  return (
    <AuthContext.Provider value={{ currentUser, setCurrentUser, newForumMessage, setNewForumMessage }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;



