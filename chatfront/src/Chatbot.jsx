import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import AuthContext from './AuthContext';
import NavigationBar from './NavigationBar';
import { useNavigate } from 'react-router-dom';
import './Chatbot.css';

function Chatbot() {
    const [messages, setMessages] = useState(() => {
        const savedMessages = localStorage.getItem('chatMessages');
        return savedMessages ? JSON.parse(savedMessages) : [];
    });

    const [showHelp, setShowHelp] = useState(() => {
        const savedShowHelp = localStorage.getItem('showHelp');
        return savedShowHelp ? JSON.parse(savedShowHelp) : false;
    });

    const axiosInstance = axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    });

    const handleClearMessages = () => {
        setMessages([]);
        localStorage.removeItem('chatMessages');
    };

    const navigate = useNavigate();

    const handleSubmitMessage = (message) => {
        const newUserMessage = { text: message, from: 'user' };
        const updatedMessages = [...messages, newUserMessage];
        setMessages(updatedMessages);
        localStorage.setItem('chatMessages', JSON.stringify(updatedMessages));

        setShowHelp(false); // Ocultar la ayuda cuando se envía un mensaje
        localStorage.setItem('showHelp', JSON.stringify(false));

        axiosInstance.get(`/api/chatbot_response/?message=${encodeURIComponent(message)}`)
            .then(response => {
                const suggestion = response.data.suggestion;
                const newBotMessage = { text: response.data.response, from: 'bot',suggestion: suggestion };
                const updatedMessagesWithBot = [...updatedMessages, newBotMessage];
                setMessages(updatedMessagesWithBot);
                localStorage.setItem('chatMessages', JSON.stringify(updatedMessagesWithBot));

                if (response.data.is_finished) {
                    setTimeout(() => {
                        alert('Flujo terminado con una nota de ' + response.data.mark);
                        handleClearMessages();
                        navigate('/menu');
                    }, 2000); 
                }
            })
            .catch(error => {
                console.log(error);
            });
    };

    const restartFlow = () => {
        axiosInstance.get(`/api/restart_flow`)
            .then(response => {
                console.log('Flow restarted');
            })
            .catch(error => {
                console.log(error);
            });
    };

    useEffect(() => {
        axiosInstance.get(`/api/check_chatbot`)
        .then(response => {
            const chatbot = response.data.chatbot;
            if (!chatbot){
                navigate('/menu');
                alert('Escoge un flujo antes de interactuar con el bot !');
            }
        })
        .catch(error => {
            console.log(error);
        });
    }, []);

    useEffect(() => {
        localStorage.setItem('chatMessages', JSON.stringify(messages));
    }, [messages]);

    return (
        <div className="chatbot">
            <NavigationBar/>
            <ChatHeader handleClearMessages={handleClearMessages} restartFlow={restartFlow} showHelp={showHelp} setShowHelp={setShowHelp} />
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





