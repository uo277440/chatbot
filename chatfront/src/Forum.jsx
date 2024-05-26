import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

const Forum = () => {
    const [messages, setMessages] = useState([]);
    const [content, setContent] = useState('');
    const [userId, setUserId] = useState(null);
    const websocket = useRef(null);

    useEffect(() => {
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
                setMessages(prevMessages => [...prevMessages, { message: data.message, user: data.user }]);
            };

            websocket.current.onclose = function(event) {
                console.error('WebSocket closed unexpectedly');
                websocket.current = null; // Reset the ref to null when the connection is closed
                // setTimeout(initializeWebSocket, 1000); // Retry connection after 1 second
            };
        };

        client.get('/api/user')
            .then(response => {
                setUserId(response.data.user.user_id);
                console.log('User fetched successfully');
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

    return (
        <div>
            <h1>Forum</h1>
            <ul>
                {messages.map((msg, index) => (
                    <li key={index}>
                        <strong>{msg.user.username}</strong>: {msg.message}
                    </li>
                ))}
            </ul>
            <form onSubmit={handleSubmit}>
                <textarea
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    placeholder="Write your message..."
                    required
                />
                <button type="submit">Post Message</button>
            </form>
        </div>
    );
};

export default Forum;





