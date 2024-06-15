import React, { useEffect, useState, useRef, useContext,useMemo } from 'react';
import axios from 'axios';
import '../css/Forum.css';
import NavigationBar from '../NavigationBar';
import AuthContext from './AuthContext';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;



const Forum = () => {
    const {setNewForumMessage } = useContext(AuthContext);
    const [messages, setMessages] = useState([]);
    const [pinnedMessage, setPinnedMessage] = useState(null); // Estado para el mensaje fijado
    const [content, setContent] = useState('');
    const [userId, setUserId] = useState(null);
    const [isSuperUser, setIsSuperUser] = useState(false);
    const websocket = useRef(null);
    const messagesEndRef = useRef(null);
    const client = useMemo(() => axios.create({
        baseURL: '/choreo-apis/chatbottfg/backend/v1',
        withCredentials: true
    }), []);
    const constructWebSocketURL = (baseURL) => {
        const origin = window.location.origin;
        const protocol = origin.startsWith('https') ? 'wss' : 'ws';
        return `${protocol}://${origin}${baseURL.replace('http', '')}/ws/forum/`;
    };

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await client.get('/api/forum/messages');
                setMessages(response.data.messages);
                setPinnedMessage(response.data.pinnedMessage); // Asignar mensaje fijado
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        };

        const initializeWebSocket = () => {
            if (websocket.current) {
                console.log("WebSocket already initialized");
                return;
            }

            console.log("Initializing WebSocket");
            const websocketURL = constructWebSocketURL('/choreo-apis/chatbottfg/backend/v1');
            websocket.current = new WebSocket(websocketURL);

            websocket.current.onopen = () => {
                console.log("WebSocket connected");
            };

            websocket.current.onmessage = function(event) {
                const data = JSON.parse(event.data);
                console.log('Received data:', data);
                if (data.action === 'delete') {
                    setMessages(prevMessages => prevMessages.filter(msg => msg.id !== data.id));
                } else if (data.action === 'edit') {
                    setMessages(prevMessages => prevMessages.map(msg => 
                        msg.id === data.id ? { ...msg, message: data.message } : msg
                    ));
                } else if (data.action === 'pin') {
                    setPinnedMessage(data.message); // Fijar mensaje
                } else if (data.action === 'unpin') {
                    setPinnedMessage(null); // Despinar mensaje
                } else {
                    setMessages(prevMessages => [...prevMessages, { id: data.id, message: data.message, user: data.user }]);
                }
            };

            websocket.current.onclose = function(event) {
                console.error('WebSocket closed unexpectedly');
                websocket.current = null; // Reset the ref to null when the connection is closed
            };
        };

        client.get('/api/user')
            .then(response => {
                console.log('forum')
                console.log(response.data)
                setUserId(response.data.user.user_id);
                setIsSuperUser(response.data.user.is_superuser);
                fetchMessages();
                initializeWebSocket();
            })
            .catch(error => {
                console.error('Error fetching user:', error);
            });

        return () => {
            console.log("Cleaning up WebSocket");
            if (websocket.current) {
                websocket.current.close();
                websocket.current = null; // Reset the ref to null on cleanup
            }
        };
    }, []);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const handleSubmit = (event) => {
        event.preventDefault();

        if (websocket.current && websocket.current.readyState === WebSocket.OPEN) {
            websocket.current.send(JSON.stringify({ message: content, user: userId }));
            setContent('');
        } else {
            console.error('WebSocket is not open');
        }
    };

    const handleDelete = (messageId) => {
        if (websocket.current && websocket.current.readyState === WebSocket.OPEN) {
            websocket.current.send(JSON.stringify({ action: 'delete', id: messageId }));
        } else {
            console.error('WebSocket is not open');
        }
    };

    const handleEdit = (messageId) => {
        const newContent = prompt('Enter new content:');
        if (newContent) {
            if (websocket.current && websocket.current.readyState === WebSocket.OPEN) {
                websocket.current.send(JSON.stringify({ action: 'edit', id: messageId, message: newContent }));
            } else {
                console.error('WebSocket is not open');
            }
        }
    };

    const handlePin = (messageId) => {
        if (websocket.current && websocket.current.readyState === WebSocket.OPEN) {
            websocket.current.send(JSON.stringify({ action: 'pin', id: messageId }));
        } else {
            console.error('WebSocket is not open');
        }
    };

    const handleUnpin = () => {
        if (websocket.current && websocket.current.readyState === WebSocket.OPEN) {
            websocket.current.send(JSON.stringify({ action: 'unpin' }));
        } else {
            console.error('WebSocket is not open');
        }
    };

    useEffect(() => {
        if (window.location.pathname === '/forumMessage') {
            setNewForumMessage(false);  
        }
    }, [setNewForumMessage]);

    return (
        <div>
            <div className="navigation-bar">
                <NavigationBar />
            </div>
            <div id="forum-container">
                <h1 id="forum-header">Foro</h1>
                {pinnedMessage && pinnedMessage.message && (
                    <div className="pinned-message">
                        <div className="message-content">
                            <strong className="message-user">{pinnedMessage.user.username}</strong>: {pinnedMessage.message}
                        </div>
                        {isSuperUser && (
                            <div className="message-actions">
                                <button onClick={handleUnpin} className="unpin-button">
                                    <img src="assets/chincheta.png" alt="Unpin" />
                                </button>
                            </div>
                        )}
                    </div>
                )}
                <ul id="forum-messages">
                    {messages.map((msg, index) => (
                        <li key={index} className={`forum-message ${msg.user.user_id === userId ? 'own-message' : ''}`}>
                            <div className="message-content">
                                <strong className="message-user">{msg.user.username}</strong>: {msg.message}
                            </div>
                            <div className="message-actions">
                                {msg.user.user_id === userId && (
                                    <button onClick={() => handleEdit(msg.id)} className="edit-button">
                                        <img src="/assets/editar.png" alt="Edit" />
                                    </button>
                                )}
                                {(msg.user.user_id === userId || isSuperUser) && (
                                    <button onClick={() => handleDelete(msg.id)} className="delete-button">
                                        <img src="/assets/borrar.png" alt="Delete" />
                                    </button>
                                )}
                                {isSuperUser && msg.user.user_id === userId &&(
                                    <button onClick={() => handlePin(msg.id)} className="pin-button">
                                        <img src="/assets/chincheta.png" alt="Pin" />
                                    </button>
                                )}
                            </div>
                        </li>
                    ))}
                    <div ref={messagesEndRef} />
                </ul>
                <form onSubmit={handleSubmit} id="forum-form">
                    <textarea
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        placeholder="Escribe tu mensaje ..."
                        required
                        id="message-input"
                    />
                    <button type="submit" id="submit-button">Enviar</button>
                </form>
            </div>
        </div>
    );
};

export default Forum;








