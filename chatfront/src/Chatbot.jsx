import React, { useState, useContext  } from 'react';
import axios from 'axios';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import Mascot from './Mascot';
import AuthContext from './AuthContext';
import NavigationBar from './NavigationBar';
import { useNavigate } from 'react-router-dom';
import './Chatbot.css';

function Chatbot() {
    const [messages, setMessages] = useState([]);
    const { currentUser, setCurrentUser } = useContext(AuthContext)
    const navigate = useNavigate();
    const axiosInstance = axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    });
    const handleClearMessages = () => {
        setMessages([]);
    };

    const handleSubmitMessage = (message) => {
        const newUserMessage = { text: message, from: 'user' };
        setMessages([...messages, newUserMessage]);
        axiosInstance.get(`/api/chatbot_response/?message=${encodeURIComponent(message)}`)
            .then(response => {
                const newBotMessage = { text: response.data.response, from: 'bot' };
                setMessages([...messages, newUserMessage, newBotMessage]);
            })
            .catch(error => {
                console.log(error);
            });
    };
    const restartFlow = () => {
        axiosInstance.get(`/api/restart_flow`)
            .then(response => {
                console.log('hola')
            })
            .catch(error => {
                console.log(error);
            });
    };
    function handleLogout(e) {
        e.preventDefault();
        axiosInstance.post(
          "/api/logout",
          { withCredentials: true }
        ).then(function (res) {
          setCurrentUser(false);
          navigate('/')
        });
      }
    
   

    return (
        <div className="chatbot">
            <NavigationBar
                currentUser={currentUser}
                handleLogout={handleLogout}
            />
            <ChatHeader handleClearMessages={handleClearMessages} restartFlow={restartFlow}/>
            <div className="messages-section">
                <ChatMessages messages={messages} setMessages={setMessages}/>
            </div>
            <div className="input-section">
                <ChatInput onSubmit={handleSubmitMessage}/>
            </div>
            
        </div>
        
    );
}

export default Chatbot;



