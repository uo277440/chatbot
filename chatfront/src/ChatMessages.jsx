import React, { useEffect, useRef } from 'react';
import './ChatMessages.css';

function ChatMessages({ messages }) {
    const messagesRef = useRef(null);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    };

    return (
        <div className="chat-messages" ref={messagesRef}>
            {messages.map((message, index) => (
                <div key={index} className={`message ${message.from}`}>
                    {message.text}
                </div>
            ))}
        </div>
    );
}

export default ChatMessages;

