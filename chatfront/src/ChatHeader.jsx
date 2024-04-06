import React from 'react';
import './ChatHeader.css';
import Mascot from './Mascot';


function ChatHeader(props) {
    return (
        <div className="chat-header">
            <h1>Chatbot de Aprendizaje de Idiomas</h1>
            <Mascot/>
            <button onClick={props.handleClearMessages}>Borrar mensajes</button>
            <button onClick={props.restartFlow}>Reiniciar flujo</button>
        </div>
    );
}

export default ChatHeader;