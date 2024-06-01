import React, { useState, useEffect,useMemo} from 'react';
import axios from 'axios';
import '../css/Profile.css';
import NavigationBar from '../NavigationBar';

function Profile() {
    const [profileData, setProfileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const axiosInstance = useMemo(() => axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
      }), []);

    useEffect(() => {
        axiosInstance.get('/api/user_profile')
            .then(response => {
                console.log('profile')
                setProfileData(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching profile data:', error);
                setLoading(false);
            });
    }, [axiosInstance]);

    const getMarkClass = (mark) => {
        if (mark >= 0 && mark <= 4) {
            return 'low-mark';
        } else if (mark >= 5 && mark <= 7) {
            return 'medium-mark';
        } else if (mark >= 8 && mark <= 10) {
            return 'high-mark';
        } else {
            return '';
        }
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!profileData) {
        return <div>No data available</div>;
    }

    return (
        <div className="profile">
            <NavigationBar/>
            <h1>Perfil de Usuario</h1>
            <div className="user-info">
                <h2>Información del Usuario</h2>
                <p><strong>Nombre de usuario:</strong> {profileData.user.username}</p>
                <p><strong>Correo electrónico:</strong> {profileData.user.email}</p>
            </div>
            <div className="marks-info">
                <h2>Notas Medias</h2>
                {profileData.average_marks.length > 0 ? (
                    <ul>
                        {profileData.average_marks.map((mark, index) => (
                            <li key={index} className={getMarkClass(mark.average_mark)}>
                                <p><strong>Escenario:</strong> {mark.flow.scenery.name}</p>
                                <p><strong>Flujo:</strong> {mark.flow.name}</p>
                                <p><strong>Nota media:</strong> {mark.average_mark.toFixed(2)}</p>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No hay notas disponibles</p>
                )}
            </div>
        </div>
    );
}

export default Profile;
