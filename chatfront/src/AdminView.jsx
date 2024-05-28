import React, { useState, useContext, useEffect } from 'react';
import axios from 'axios';
import AuthContext from './AuthContext';
import './Admin.css';
import NavigationBar from './NavigationBar';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function AdminView() {
  const [file, setFile] = useState(null);
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState('');
  const [newScenario, setNewScenario] = useState('');
  const [csvFile, setCSVFile] = useState(null);
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000'
  });

  useEffect(() => {
    fetchScenarios();
  }, []);

  const fetchScenarios = () => {
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

  const handleCSVChange = (event) => {
    setCSVFile(event.target.files[0]);
  };

  const handleScenarioChange = (event) => {
    setSelectedScenario(event.target.value);
  };

  const handleNewScenarioChange = (event) => {
    setNewScenario(event.target.value);
  };

  function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
  }

  const handleUpload = () => {
    if (!file) {
      alert('Seleccione un archivo JSON');
      return;
    }
    if (!csvFile) {
      alert('Seleccione un archivo CSV');
      return;
    }
    if (!selectedScenario && !newScenario) {
      alert('Seleccione un escenario existente o ingrese un nuevo escenario');
      return;
    }

    const formData = new FormData();
    formData.append('json_file', file);
    formData.append('csv_file', csvFile);
    formData.append('scenario', selectedScenario || newScenario);
    const csrftoken = getCookie('csrftoken');
    axiosInstance.post('/api/upload_combined', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': csrftoken
      }
    })
    .then(response => {
      alert('Archivos subidos y verificados correctamente');
    })
    .catch(error => {
      alert('Ha habido un error durante la subida del archivo');
    });
  };

  return (
    <div className="admin">
      <NavigationBar />
      <h2>Admin View</h2>

      <div className="upload-section">
        <label htmlFor="jsonFileInput">Subir archivo JSON (Flujo):</label>
        <input id="jsonFileInput" type="file" onChange={handleFileChange} />

        <label htmlFor="csvFileInput">Subir archivo CSV (Datos de Entrenamiento):</label>
        <input id="csvFileInput" type="file" onChange={handleCSVChange} />
      </div>

      <div className="scenario-selection">
        <label htmlFor="existingScenarioSelect">Seleccione un escenario existente:</label>
        <select id="existingScenarioSelect" onChange={handleScenarioChange}>
          <option value="">Seleccione un escenario existente</option>
          {scenarios.map(scenario => (
            <option key={scenario.id} value={scenario.id}>{scenario.name}</option>
          ))}
        </select>

        <label htmlFor="newScenarioInput">O ingrese el nombre de un nuevo escenario:</label>
        <input
          id="newScenarioInput"
          type="text"
          placeholder="Nombre del nuevo escenario"
          value={newScenario}
          onChange={handleNewScenarioChange}
        />
      </div>

      <button onClick={handleUpload}>Enviar al backend</button>
    </div>
  );
}

export default AdminView;


