import React, { useState } from 'react';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput'
function Chatbot() {
    const [messages, setMessages] = useState([]);

    const handleSubmitMessage = (message) => {
        setMessages([...messages, { text: message, from: 'user' }]);
       //lógica para comunicarse con backend y obtener respuesta del bot
    };

    return (
        <div className="chatbot">
            <ChatHeader />
            <ChatMessages messages={messages} />
            <ChatInput onSubmit={handleSubmitMessage} />
        </div>
    );
}

export default Chatbot;
