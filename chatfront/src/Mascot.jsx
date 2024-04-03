import React, { useState } from 'react';
import axios from 'axios';
import './Mascot.css';

function Mascot() {
    const [isVisible, setIsVisible] = useState(false);
    const [message, setMessage] = useState('');
    const axiosInstance = axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    });
    const handleMascotClick = () => {
        axiosInstance.get('/api/mascot_message')
            .then(response => {
                setMessage(response.data.response);
                setIsVisible(true);
            })
            .catch(error => {
                console.error('Error fetching mascot message:', error);
            });
    };

    const handleCloseMascot = () => {
        setIsVisible(false);
    };

    return (
        <div className="mascot-container">
            <button onClick={handleMascotClick}>Help</button>
            {isVisible && (
                <div>
                    <p className="mascot-message">{message}</p>
                    <button onClick={handleCloseMascot}>Close</button>
                </div>
            )}
        </div>
    );
}

export default Mascot;


