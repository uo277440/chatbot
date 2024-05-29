import React, { useEffect, useState, useRef,useContext  } from 'react';
import axios from 'axios';
import './Forum.css';
import NavigationBar from './NavigationBar';
import AuthContext from './AuthContext';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

const Forum = () => {
    const { currentUser, newForumMessage, setNewForumMessage } = useContext(AuthContext);
    const [messages, setMessages] = useState([]);
    const [content, setContent] = useState('');
    const [userId, setUserId] = useState(null);
    const [isSuperUser, setIsSuperUser] = useState(false);
    const websocket = useRef(null);

    useEffect(() => {
        const fetchMessages = async () => {
            try {
                const response = await client.get('/api/forum/messages');
                setMessages(response.data);
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
            websocket.current = new WebSocket('ws://localhost:8000/ws/forum/');

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
                } else {
                    setMessages(prevMessages => [...prevMessages, { id: data.id, message: data.message, user: data.user }]);
                }
            };


            websocket.current.onclose = function(event) {
                console.error('WebSocket closed unexpectedly');
                websocket.current = null; // Reset the ref to null when the connection is closed
                // setTimeout(initializeWebSocket, 1000); // Retry connection after 1 second
            };
        };

        client.get('/api/user')
            .then(response => {
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
    useEffect(() => {
        if (window.location.pathname === '/forumMessage') {
            setNewForumMessage(false);  
        }
    }, [window.location.pathname]);

    return (
        <div id="forum-container">
            <NavigationBar/>
            <h1 id="forum-header">Foro</h1>
            <ul id="forum-messages">
                {messages.map((msg, index) => (
                     <li key={index} className={`forum-message ${msg.user.user_id === userId ? 'own-message' : ''}`}>
                    <div className="message-content">
                        <strong className="message-user">{msg.user.username}</strong>: {msg.message}
                    </div>
                    {(msg.user.user_id === userId || isSuperUser) && (
                        <div className="message-actions">
                            {msg.user.user_id === userId && (
                                 <button onClick={() => handleEdit(msg.id)} className="edit-button">
                                    <img src="/multimedia/editar.png" alt="Edit" />
                                </button>
                            )}
                            <button onClick={() => handleDelete(msg.id)} className="delete-button">
                                <img src="/multimedia/borrar.png" alt="Delete" />
                            </button>
                        </div>
                    )}
                </li>
            ))}
        </ul>
            <form onSubmit={handleSubmit} id="forum-form">
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Write your message..."
                    required
                    id="message-input"
                />
                <button type="submit" id="submit-button">Enviar</button>
            </form>
        </div>
    );
};

export default Forum;






