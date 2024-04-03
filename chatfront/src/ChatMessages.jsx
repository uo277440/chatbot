import React, { useEffect, useRef, useState  } from 'react';
import axios from 'axios';
import './ChatMessages.css';
import altavoz from './assets/altavoz.png';

function ChatMessages({ messages }) {
    const messagesRef = useRef(null);
    const axiosInstance = axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    });
    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    };
    const [isButtonEnabled, setIsButtonEnabled] = useState(true);

    const handleTextToAudio = (text) => {
        if (!isButtonEnabled) return; 
        setIsButtonEnabled(false); 
        axiosInstance.get(`api/transform?text=${encodeURIComponent(text)}`)
            .then(response => {
                console.log('Respuesta de text_to_audio:', response);
                setTimeout(() => {
                    setIsButtonEnabled(true); 
                }, 10000);
            })
            .catch(error => {
                console.error('Error al llamar a text_to_audio:', error);
                setIsButtonEnabled(true); 
            });
    };

    return (
        <div className="chat-messages" ref={messagesRef}>
            {messages.map((message, index) => (
                <div key={index} className={`message ${message.from}`}>
                    <div>{message.text}</div>
                    <img
                        src={altavoz}
                        alt="Altavoz"
                        onClick={() => handleTextToAudio(message.text)}
                        className={`image-button ${isButtonEnabled ? '' : 'disabled'}`}
                    />
                </div>
            ))}
        </div>
    );
}

export default ChatMessages;


