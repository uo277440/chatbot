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
    const axiosInstance = axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    });
    const handleClearMessages = () => {
        setMessages([]);
    };
    const navigate = useNavigate();

    const handleSubmitMessage = (message) => {
        const newUserMessage = { text: message, from: 'user' };
        setMessages([...messages, newUserMessage]);
        axiosInstance.get(`/api/chatbot_response/?message=${encodeURIComponent(message)}`)
            .then(response => {
                const newBotMessage = { text: response.data.response, from: 'bot' };
                setMessages([...messages, newUserMessage, newBotMessage]);
                if(response.data.is_finished){
                    alert('Flujo terminado con una nota de '+response.data.mark)
                    navigate('/menu')
                }
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
   

    return (
        <div className="chatbot">
            <NavigationBar/>
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



