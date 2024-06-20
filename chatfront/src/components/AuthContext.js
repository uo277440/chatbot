import React, { createContext, useState, useEffect, useRef } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(() => {
    const savedUser = localStorage.getItem('currentUser');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [newForumMessage, setNewForumMessage] = useState(false);



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
    console.log('no paro')
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

  }, [currentUser]);

  return (
    <AuthContext.Provider value={{ currentUser, setCurrentUser, newForumMessage, setNewForumMessage }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;





