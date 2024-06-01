import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../css/Mascot.css';

function Mascot({ showHelp, setShowHelp }) {
    const [message, setMessage] = useState(() => {
        const savedMessage = localStorage.getItem('mascotMessage');
        return savedMessage ? savedMessage : '';
    });

    const axiosInstance = axios.create({
        baseURL: 'http://127.0.0.1:8000',
        withCredentials: true
    });

    const handleMascotClick = () => {
        axiosInstance.get('/api/mascot_message')
            .then(response => {
                setMessage(response.data.response);
                setShowHelp(true);
                localStorage.setItem('mascotMessage', response.data.response);
                localStorage.setItem('showHelp', JSON.stringify(true));
            })
            .catch(error => {
                console.error('Error fetching mascot message:', error);
            });
    };
   
    const handleCloseMascot = () => {
        setShowHelp(false);
        localStorage.setItem('showHelp', JSON.stringify(false));
    };

    useEffect(() => {
        if (!showHelp) {
            setMessage('');
            localStorage.removeItem('mascotMessage');
        }
    }, [showHelp]);

    return (
        <div className="mascot-container">
            {!showHelp && (
                <button onClick={handleMascotClick}>Help</button>
            )}
            {showHelp && (
                <div>
                    <p className="mascot-message">{message}</p>
                </div>
            )}
        </div>
    );
}

export default Mascot;




