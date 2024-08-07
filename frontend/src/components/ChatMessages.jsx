import React, { useEffect, useRef, useState, useMemo } from 'react';
import axios from 'axios';
import '../css/ChatMessages.css';
import altavoz from '../assets/altavoz.png';
import traducir from '../assets/translate.png';

function ChatMessages({ messages, setMessages }) {
    const messagesRef = useRef(null);
    const axiosInstance = useMemo(() => axios.create({
        baseURL: '/choreo-apis/chatbottfg/backend/v1',
        withCredentials: true
    }), []);

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const scrollToBottom = () => {
        messagesRef.current.scrollTop = messagesRef.current.scrollHeight;
    };

    const [isButtonEnabled, setIsButtonEnabled] = useState(true);

    const handleTextToAudio = (text, lang) => {
        if (!isButtonEnabled) return;
        setIsButtonEnabled(false);
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang || 'en';
        utterance.onend = () => {
            setIsButtonEnabled(true);
        };
        utterance.onerror = (error) => {
            console.error('Error in speech synthesis:', error);
            setIsButtonEnabled(true);
        };
        window.speechSynthesis.speak(utterance);
    };

    const handleTranslate = (text, lang, index) => {
        const sourceLang = lang || 'en';
        const targetLang = sourceLang === 'en' ? 'es' : 'en';
        axiosInstance.get(`api/translate?text=${encodeURIComponent(text)}&target=${targetLang}`)
            .then(response => {
                const translatedText = response.data.translated_text;
                console.log('Respuesta de handleTranslate:', translatedText);
                const updatedMessages = [...messages];
                updatedMessages[index].text = translatedText;
                updatedMessages[index].lang = targetLang;
                setMessages(updatedMessages);
            })
            .catch(error => {
                console.error('Error al llamar a text_to_audio:', error);
            });
    };

    return (
        <div className="chat-messages" ref={messagesRef}>
            {messages.map((message, index) => (
                <div 
                    key={index} 
                    className={`message ${message.from} ${message.suggestion ? 'suggestion' : ''}`} 
                    lang={message.lang || 'en'}
                >
                    {message.text.split('\n').map((line, idx) => (
                        <p key={idx}>{line}</p>
                    ))}
                    {!message.suggestion && (
                        <img
                            src={altavoz}
                            alt="Altavoz"
                            onClick={() => handleTextToAudio(message.text, message.lang)}
                            className={`image-button ${isButtonEnabled ? '' : 'disabled'}`}
                        />
                    )}
                    {message.from === 'bot' && !message.suggestion && (
                        <img
                            src={traducir}
                            alt="Traducir"
                            onClick={() => handleTranslate(message.text, message.lang, index)}
                            className={'image-button'}
                        />
                    )}
                </div>
            ))}
        </div>
    );
}

export default ChatMessages;





