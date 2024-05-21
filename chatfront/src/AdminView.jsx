import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import AuthContext from './AuthContext';
import './Admin.css';
import NavigationBar from './NavigationBar';
function AdminView() {
  const [file, setFile] = useState(null);
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState('');
  const [newScenario, setNewScenario] = useState('');
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true
});

  useEffect(() => {
    // Fetch existing scenarios when component mounts
    fetchScenarios();
  }, []);

  const fetchScenarios = () => {
    // Fetch existing scenarios from the backend
    axiosInstance.get('/api/scenarios')
      .then(response => {
        setScenarios(response.data.scenarios);
      })
      .catch(error => {
        console.error('Error fetching scenarios:', error);
      });
  };

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleScenarioChange = (event) => {
    setSelectedScenario(event.target.value);
  };

  const handleNewScenarioChange = (event) => {
    setNewScenario(event.target.value);
  };

  const handleUpload = () => {
    if (!file) {
      alert('Seleccione un archivo JSON');
      return;
    }

    if (!selectedScenario && !newScenario) {
      alert('Seleccione un escenario existente o ingrese un nuevo escenario');
      return;
    }

    const formData = new FormData();
    formData.append('json_file', file);

    // Append selected scenario or new scenario to form data
    formData.append('scenario', selectedScenario || newScenario);

    axiosInstance.post('/api/upload_scenary', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
        alert('El JSON se ha subido correctamente');
    })
    .catch(error => {
        alert('Ha habido un error durante la subida del archivo');
    });
  };

  return (
    <div className="admin">
      <NavigationBar/>
      <h2>Admin View</h2>
      <input type="file" onChange={handleFileChange} />
      
      {/* Dropdown for selecting existing scenarios */}
      <select onChange={handleScenarioChange}>
        <option value="">Seleccione un escenario existente</option>
        {scenarios.map(scenario => (
          <option key={scenario.id} value={scenario.id}>{scenario.name}</option>
        ))}
      </select>

      {/* Input field for entering a new scenario name */}
      <input type="text" placeholder="Nombre del nuevo escenario" value={newScenario} onChange={handleNewScenarioChange} />
      
      <button onClick={handleUpload}>Enviar al backend</button>
    </div>
  );
}

export default AdminView;

