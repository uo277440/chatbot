import React, { useState, useEffect } from 'react';
import '../css/ChatInput.css'; // Estilos CSS personalizados
import micro from '../assets/micro.png';

function ChatInput({ onSubmit }) {
    const [message, setMessage] = useState('');
    const [isListening, setIsListening] = useState(false);
    const [isSpeechRecognitionSupported, setIsSpeechRecognitionSupported] = useState(false);

    useEffect(() => {
        // Verificar si la API de reconocimiento de voz está disponible
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        setIsSpeechRecognitionSupported(!!SpeechRecognition);
    }, []);

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    const handleChange = (event) => {
        setMessage(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        if (message.trim() !== '') {
            onSubmit(message);
            setMessage('');
        }
    };

    const handleMicrophoneClick = () => {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert('API de reconocimiento de voz no soportada por este navegador. Por favor, usa Chrome.');
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US'; 

        recognition.onstart = () => {
            console.log('Recognition started');
            setIsListening(true);
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            const capitalizedTranscript = capitalizeFirstLetter(transcript);
            console.log('Transcript:', capitalizedTranscript);
            setMessage(capitalizedTranscript);
        };

        recognition.onerror = (event) => {
            console.error('Recognition error:', event.error);
            setIsListening(false);
        };

        recognition.onend = () => {
            console.log('Recognition ended');
            setIsListening(false);
        };

        if (!isListening) {
            recognition.start();
        } else {
            recognition.stop();
        }
    };

    return (
        <form className="chat-input" onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Escribe un mensaje..."
                value={message}
                onChange={handleChange}
            />
            <button type="submit">Enviar</button>
            {isSpeechRecognitionSupported && (
                <img 
                    src={micro}
                    alt="Hablar"
                    className={'image-button'}
                    onClick={handleMicrophoneClick}
                />
            )}
        </form>
    );
}

export default ChatInput;