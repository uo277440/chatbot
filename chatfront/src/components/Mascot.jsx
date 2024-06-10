import React, { useState, useEffect,useMemo } from 'react';
import axios from 'axios';
import '../css/Mascot.css';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function Mascot({ showHelp, setShowHelp }) {
    const [message, setMessage] = useState(() => {
        const savedMessage = localStorage.getItem('mascotMessage');
        return savedMessage ? savedMessage : '';
    });

    const axiosInstance = useMemo(() => axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
      }), []);

    const handleMascotClick = () => {
        axiosInstance.get('/api/mascot_message')
            .then(response => {
                setMessage(response.data.response);
                setShowHelp(true);
                localStorage.setItem('mascotMessage', response.data.response);
                localStorage.setItem('showHelp',true);
            })
            .catch(error => {
                console.error('Error fetching mascot message:', error);
            });
    };
   

    useEffect(() => {
        if (!localStorage.getItem('showHelp')) {
            setMessage('');
            localStorage.removeItem('mascotMessage');
        }
        console.log('MASCOTA')
        console.log(localStorage.getItem('showHelp'))
    }, [showHelp]);

    return (
        <div className="mascot-container">
            {localStorage.getItem('showHelp')===JSON.stringify(false) && (
                <button onClick={handleMascotClick}>Ayuda</button>
            )}
            {localStorage.getItem('showHelp')===JSON.stringify(true) && (
                <div>
                    <p className="mascot-message">{message}</p>
                </div>
            )}
        </div>
    );
}

export default Mascot;




