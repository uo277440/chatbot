import React, { useState, useEffect,useCallback,useMemo  } from 'react';
import axios from 'axios';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import ChatInput from './ChatInput';
import NavigationBar from '../NavigationBar';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import '../css/Chatbot.css';

function Chatbot() {
    const [messages, setMessages] = useState(() => {
        const savedMessages = localStorage.getItem('chatMessages');
        return savedMessages ? JSON.parse(savedMessages) : [];
    });

    const [showHelp, setShowHelp] = useState(() => {
        const savedShowHelp = localStorage.getItem('showHelp');
        return savedShowHelp ? JSON.parse(savedShowHelp) : false;
    });

    const axiosInstance = useMemo(() => axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
      }), []);

    const handleClearMessages = () => {
        setMessages([]);
        localStorage.removeItem('chatMessages');
    };

    const navigate = useNavigate();

    const handleSubmitMessage = (message) => {
        checkBot()
        const newUserMessage = { text: message, from: 'user' };
        const updatedMessages = [...messages, newUserMessage];
        setMessages(updatedMessages);
        localStorage.setItem('chatMessages', JSON.stringify(updatedMessages));

        setShowHelp(false); // Ocultar la ayuda cuando se envía un mensaje
        localStorage.setItem('showHelp', JSON.stringify(false));

        axiosInstance.get(`/api/chatbot_response/?message=${encodeURIComponent(message)}`)
            .then(response => {
                const suggestion = response.data.suggestion;
                const newBotMessage = { text: response.data.response, from: 'bot',suggestion: suggestion };
                const updatedMessagesWithBot = [...updatedMessages, newBotMessage];
                setMessages(updatedMessagesWithBot);
                localStorage.setItem('chatMessages', JSON.stringify(updatedMessagesWithBot));

                if (response.data.is_finished) {
                    setTimeout(() => {
                        var message 
                        var icon
                        if(response.data.mark > 5){
                             message = 'Felicidades has terminado el flujo con éxito. Tu nota es un '
                             icon='success'
                        }else{
                             message = 'Debes practicar más. Tu nota es un '
                             icon='error'
                        }
                        Swal.fire({
                            title: 'Nota del flujo',
                            text: message+ response.data.mark,
                            icon: icon,
                            confirmButtonText: 'Aceptar'
                        });
                        handleClearMessages();
                        navigate('/menu');
                    }, 2000); 
                }
            })
            .catch(error => {
                console.log(error);
            });
    };

    const restartFlow = () => {
        axiosInstance.get(`/api/restart_flow`)
            .then(response => {
                console.log('Flow restarted');
            })
            .catch(error => {
                console.log(error);
            });
    };
    const checkBot = useCallback(() => {
        axiosInstance.get(`/api/check_chatbot`)
        .then(response => {
            const chatbot = response.data.chatbot;
            const description = response.data.description;
            if (!chatbot){
                navigate('/menu');
                Swal.fire({
                    title: 'Flujo no seleccionado',
                    text: 'Escoge un flujo antes de interactuar con el bot !',
                    icon: 'error',
                    confirmButtonText: 'Aceptar'
                });
            }else{
                if((localStorage.getItem('first'))==JSON.stringify(true)){
                    Swal.fire({
                        title: 'Descripción del flujo',
                        text: description,
                        icon: 'info',
                        confirmButtonText: 'Aceptar'
                    });
                    localStorage.setItem('first', JSON.stringify(false));
                }
                
            }
        })
        .catch(error => {
            console.log(error);
        });
    }, [navigate, axiosInstance]);
        

    useEffect(() => {
        checkBot()
        localStorage.setItem('chatMessages', JSON.stringify(messages));
    }, [messages,checkBot]);

    return (
        <div className="chatbot">
            <NavigationBar/>
            <ChatHeader handleClearMessages={handleClearMessages} restartFlow={restartFlow} showHelp={showHelp} setShowHelp={setShowHelp} />
            <div className="messages-section">
                <ChatMessages messages={messages} setMessages={setMessages}/>
            </div>
            <div className="input-section">
                <ChatInput onSubmit={handleSubmitMessage}/>
            </div>
        </div>
    );
}

export default Chatbot;





