import React from 'react';
import '../css/ChatHeader.css';
import Mascot from './Mascot';

function ChatHeader({ handleClearMessages, restartFlow, showHelp, setShowHelp }) {
    return (
        <div className="chat-header">
            <h1>Chatbot de Aprendizaje de Idiomas</h1>
            <Mascot showHelp={showHelp} setShowHelp={setShowHelp} />
            <button onClick={handleClearMessages}>Borrar mensajes</button>
            <button onClick={restartFlow}>Reiniciar flujo</button>
        </div>
    );
}

export default ChatHeader;
