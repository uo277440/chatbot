import React, { useState, useMemo } from 'react';
import axios from 'axios';
import '../css/AdminMarks.css';
import NavigationBar from '../NavigationBar';
import downloadIcon from '../assets/descargar.png';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function AdminMarks() {
    const [username, setUsername] = useState('');
    const [user, setUser] = useState(null);
    const [marks, setMarks] = useState([]);
    const [conversations, setConversations] = useState([]);
    const axiosInstance = useMemo(() => axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    }), []);

    const handleSearch = () => {
        axiosInstance.get(`/api/search_student/?search_param=${username}`)
            .then(response => {
                console.log(response.data.conversations); 
                setUser(response.data.user);
                setMarks(response.data.marks);
                setConversations(response.data.conversations);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
                setUser(null);
                setMarks([]);
                setConversations([]);
                alert('No se encontró ningun usuario');
            });
    };

    const getMarkClass = (mark) => {
        if (mark < 5) return 'mark-red';
        if (mark >= 5 && mark <= 7) return 'mark-yellow';
        if (mark >= 8 && mark <= 10) return 'mark-green';
        return '';
    };

    const downloadConversation = (conversation, date) => {
        const element = document.createElement('a');
        let fileContent = '';

        // Intentar convertir a un array si es necesario
        let messages = conversation;
        if (typeof conversation === 'string') {
            try {
                messages = JSON.parse(conversation);
            } catch (e) {
                console.error('Error parsing conversation JSON:', e);
            }
        }

        // Asegurarse de que `messages` sea un array
        if (Array.isArray(messages)) {
            messages.forEach(message => {
                const from = message.from === 'user' ? 'User: ' : 'Bot: ';
                fileContent += `${from}${message.text}\n`;
            });
        } else {
            console.error('Conversation is not an array:', messages);
        }
        fileContent += `\nFecha: ${date}\n`;

        const file = new Blob([fileContent], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = 'chat_conversation.txt';
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    return (
        <div>
            <div className="navigation-bar">
                <NavigationBar />
            </div>
            <div className="admin-view">
                <h1>Buscar Alumnos</h1>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Nombre de usuario"
                />
                <button onClick={handleSearch}>Buscar</button>

                {user && (
                    <div>
                        <h2>Detalles del Usuario</h2>
                        <p>Nombre: {user.username}</p>
                        <p>Email: {user.email}</p>

                        <h2>Notas</h2>
                        {marks.length > 0 ? (
                            <ul>
                                {marks.map(mark => (
                                    <li key={mark.id} className={getMarkClass(mark.mark)}>
                                        Escenario: {mark.flow.scenery.name} - Flujo: {mark.flow.name} - Nota: {mark.mark} - Fecha: {mark.date}
                                        <button className="download-button" onClick={() => downloadConversation(conversations[mark.id], mark.date)}>
                                            <img src={downloadIcon} alt="Download" className="download-icon" />
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>Este usuario no tiene notas registradas.</p>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default AdminMarks;


