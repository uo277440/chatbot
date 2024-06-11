import React, { createContext, useState, useEffect, useRef,useMemo } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(() => {
    const savedUser = localStorage.getItem('currentUser');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const axiosInstance = useMemo(() => axios.create({
    baseURL: 'http://chatbot-tfg-863d13080855.herokuapp.com',
    withCredentials: true
}), []);
  const [newForumMessage, setNewForumMessage] = useState(false);

  const websocket = useRef(null);


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
        const response = await axiosInstance.get('/api/user');
        setCurrentUser(response.data.user);
      } catch (error) {
        console.error('Error fetching user:', error);
      }
    };

    if (!currentUser) {
      fetchCurrentUser();
    }

    const connectWebSocket = () => {
      if (websocket.current) {
        websocket.current.close();
        websocket.current = null; 
    }

      websocket.current = new WebSocket('ws://localhost:8000/ws/forum/');

      websocket.current.onopen = () => {
        console.log('WebSocket connected');
      };

      websocket.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.action === 'send') {
          if (parseInt(data.user.user_id) !== parseInt(currentUser?.user_id)) {
            setNewForumMessage(true);
          }else{
            console.log('falso')
            setNewForumMessage(false);
          }
        }
      };

      websocket.current.onclose = function(event) {
        console.error('WebSocket closed unexpectedly');
        websocket.current = null; 
    };

      websocket.current.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (websocket.current) {
          websocket.current.close();
        }
      };
    };

    connectWebSocket();

    return () => {
      if (websocket.current) {
        websocket.current.onclose = null;
        websocket.current.onerror = null;
        websocket.current.close();
        websocket.current = null;
      }
    };
  }, [currentUser]);

  return (
    <AuthContext.Provider value={{ currentUser, setCurrentUser, newForumMessage, setNewForumMessage }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;





