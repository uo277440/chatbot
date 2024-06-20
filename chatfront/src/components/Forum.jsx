import React, { useEffect, useState, useRef, useContext, useMemo } from 'react';
import { collection, addDoc, onSnapshot, query, orderBy, doc, deleteDoc, updateDoc, where, getDocs } from 'firebase/firestore';
import { db } from '../firebaseConfig';
import '../css/Forum.css';
import NavigationBar from '../NavigationBar';
import AuthContext from './AuthContext';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const Forum = () => {
    const { setNewForumMessage } = useContext(AuthContext);
    const [messages, setMessages] = useState([]);
    const [pinnedMessage, setPinnedMessage] = useState(null); // Estado para el mensaje fijado
    const [content, setContent] = useState('');
    const [userId, setUserId] = useState(null);
    const [isSuperUser, setIsSuperUser] = useState(false);
    const messagesEndRef = useRef(null);
    const axiosInstance = useMemo(() => axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    }), []);

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axiosInstance.get('/api/user');
                setUserId(response.data.user.user_id);
                setIsSuperUser(response.data.user.is_superuser);
            } catch (error) {
                console.error('Error fetching user:', error);
            }
        };

        fetchUser();
    }, [axiosInstance]);

    useEffect(() => {
        const messagesQuery = query(collection(db, 'messages'), orderBy('timestamp'));
        const unsubscribeMessages = onSnapshot(messagesQuery, (snapshot) => {
            const fetchedMessages = snapshot.docs.map(doc => ({
                id: doc.id,
                ...doc.data()
            }));
            setMessages(fetchedMessages);
        });

        const pinnedQuery = query(collection(db, 'messages'), where('isPinned', '==', true));
        const unsubscribePinned = onSnapshot(pinnedQuery, (snapshot) => {
            if (!snapshot.empty) {
                const pinnedDoc = snapshot.docs[0];
                setPinnedMessage({ id: pinnedDoc.id, ...pinnedDoc.data() });
            } else {
                setPinnedMessage(null);
            }
        });

        return () => {
            unsubscribeMessages();
            unsubscribePinned();
        };
    }, []);

    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    function getCookie(name) {
        const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }

    const handleSubmit = async (event) => {
        event.preventDefault();
        if (content.trim() === '') return;

        const csrftoken = getCookie('csrftoken');
        const formData = new FormData();
        formData.append('action', 'send');
        formData.append('user_id', userId);
        formData.append('message', content);

        try {
            await axiosInstance.post('/api/forum', formData, {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
            setContent('');
        } catch (error) {
            console.error('Error sending message:', error);
        }
    };

    const handleDelete = async (messageId) => {
        const csrftoken = getCookie('csrftoken');
        const formData = new FormData();
        formData.append('action', 'delete');
        formData.append('id', messageId);

        try {
            await axiosInstance.post('/api/forum', formData, {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
        } catch (error) {
            console.error('Error deleting message:', error);
        }
    };

    const handleEdit = async (messageId) => {
        const newContent = prompt('Enter new content:');
        if (newContent) {
            const csrftoken = getCookie('csrftoken');
            const formData = new FormData();
            formData.append('action', 'edit');
            formData.append('id', messageId);
            formData.append('message', newContent);

            try {
                await axiosInstance.post('/api/forum', formData, {
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                });
            } catch (error) {
                console.error('Error editing message:', error);
            }
        }
    };

    const handlePin = async (messageId) => {
        const csrftoken = getCookie('csrftoken');
        const formData = new FormData();
    
        // Unpin the currently pinned message if it exists
        if (pinnedMessage) {
            const unpinFormData = new FormData();
            unpinFormData.append('action', 'unpin');
            unpinFormData.append('id', pinnedMessage.id);
    
            try {
                await axiosInstance.post('/api/forum', unpinFormData, {
                    headers: {
                        'X-CSRFToken': csrftoken
                    }
                });
            } catch (error) {
                console.error('Error unpinning message:', error);
            }
        }
    
        // Pin the new message
        formData.append('action', 'pin');
        formData.append('id', messageId);
    
        try {
            await axiosInstance.post('/api/forum', formData, {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
        } catch (error) {
            console.error('Error pinning message:', error);
        }
    };
    

    const handleUnpin = async () => {
        const csrftoken = getCookie('csrftoken');
        const formData = new FormData();
        formData.append('action', 'unpin');

        try {
            await axiosInstance.post('/api/forum', formData, {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            });
        } catch (error) {
            console.error('Error unpinning message:', error);
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
                            <strong className="message-user">{pinnedMessage.username}</strong>: {pinnedMessage.message}
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
                        <li key={index} className={`forum-message ${msg.user_id === userId ? 'own-message' : ''}`}>
                            <div className="message-content">
                                <strong className="message-user">{msg.username}</strong>: {msg.message}
                            </div>
                            <div className="message-actions">
                                {msg.user_id === userId && (
                                    <button onClick={() => handleEdit(msg.id)} className="edit-button">
                                        <img src="/assets/editar.png" alt="Edit" />
                                    </button>
                                )}
                                {(msg.user_id === userId || isSuperUser) && (
                                    <button onClick={() => handleDelete(msg.id)} className="delete-button">
                                        <img src="/assets/borrar.png" alt="Delete" />
                                    </button>
                                )}
                                {isSuperUser && (
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