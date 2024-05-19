import React, { useState } from 'react';
import axios from 'axios';
import './AdminMarks.css';

function AdminMarks() {
    const [username, setUsername] = useState('');
    const [user, setUser] = useState(null);
    const [marks, setMarks] = useState([]);
    const axiosInstance = axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    });
    const handleSearch = () => {
        axiosInstance.get(`/api/search_student/?username=${username}`)
            .then(response => {
                setUser(response.data.user);
                setMarks(response.data.marks);
            })
            .catch(error => {
                console.error('Error fetching user data:', error);
                setUser(null);
                setMarks([]);
            });
    };

    return (
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
                                <li key={mark.id}>
                                    Escenario: {mark.flow.scenery.name} - Flujo: {mark.flow.name} - Nota: {mark.mark}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>Este usuario no tiene notas registradas.</p>
                    )}
                </div>
            )}
        </div>
    );
}

export default AdminMarks;
