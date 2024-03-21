import React, { useState } from 'react';
import './ChatInput.css'; // Estilos CSS personalizados

function ChatInput({ onSubmit }) {
    const [message, setMessage] = useState('');

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

    return (
        <form className="chat-input" onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Escribe un mensaje..."
                value={message}
                onChange={handleChange}
            />
            <button type="submit">Enviar</button>
        </form>
    );
}

export default ChatInput;