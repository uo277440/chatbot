import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import Mascot from './Mascot';

function Chatbot() {
    const [messages, setMessages] = useState([]);
    

    const handleSubmitMessage = (message) => {
        const newUserMessage = { text: message, from: 'user' };
        setMessages([...messages, newUserMessage]);
        axios.get(`http://localhost:8000/api/chatbot_response/?message=${encodeURIComponent(message)}`)
            .then(response => {
                const newBotMessage = { text: response.data.response, from: 'bot' };
                setMessages([...messages, newUserMessage, newBotMessage]);
            })
            .catch(error => {
                console.log(error);
            });
    };
   

    return (
        <div className="chatbot">
            <ChatHeader />
            <div className="mascot-section">
                <Mascot/>
            </div>
            <div className="messages-section">
                <ChatMessages messages={messages} />
            </div>
            <div className="input-section">
                <ChatInput onSubmit={handleSubmitMessage} />
            </div>
            
        </div>
        
    );
}

export default Chatbot;



