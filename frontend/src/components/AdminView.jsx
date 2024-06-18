import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import '../css/Admin.css';
import NavigationBar from '../NavigationBar';
import Cookies from 'js-cookie';
import Swal from 'sweetalert2';
import { Dimmer, Loader, Segment } from 'semantic-ui-react';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

function AdminView() {
  const [file, setFile] = useState(null);
  const [scenarios, setScenarios] = useState([]);
  const [selectedScenario, setSelectedScenario] = useState('');
  const [newScenario, setNewScenario] = useState('');
  const [csvFile, setCSVFile] = useState(null);
  const [flows, setFlows] = useState([]);
  const [selectedFlow, setSelectedFlow] = useState('');
  const [loading, setLoading] = useState(false); // Loader state

  const axiosInstance = useMemo(() => axios.create({
    baseURL: '/choreo-apis/chatbottfg/backend/v1',
    withCredentials: true
  }), []);

  useEffect(() => {
    const csrftoken = Cookies.get('csrftoken');
    axiosInstance.defaults.headers.common['X-CSRFToken'] = csrftoken;
  }, [axiosInstance]);

  const fetchScenarios = useCallback(() => {
    axiosInstance.get('/api/scenarios')
      .then(response => {
        setScenarios(response.data.scenarios);
      })
      .catch(error => {
        console.error('Error fetching scenarios:', error);
      });
  }, [axiosInstance]);

  const fetchFlows = useCallback((scenarioId) => {
    axiosInstance.get(`/api/scenarios/${scenarioId}/flows`)
      .then(response => {
        setFlows(response.data.flows);
      })
      .catch(error => {
        console.error('Error fetching flows:', error);
      });
  }, [axiosInstance]);

  useEffect(() => {
    fetchScenarios();
  }, [fetchScenarios]);

  useEffect(() => {
    if (selectedScenario) {
      fetchFlows(selectedScenario);
    }
  }, [selectedScenario, fetchFlows]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleCSVChange = (event) => {
    setCSVFile(event.target.files[0]);
  };

  const handleScenarioChange = (event) => {
    setSelectedScenario(event.target.value);
  };

  const handleFlowChange = (event) => {
    setSelectedFlow(event.target.value);
  };

  const handleNewScenarioChange = (event) => {
    setNewScenario(event.target.value);
  };

  const handleUpload = (event) => {
    event.preventDefault();
    

    if (!file) {
      Swal.fire({
        title: 'Datos faltantes',
        text: "Seleccione un fichero JSON",
        icon: 'error',
        confirmButtonText: 'Aceptar'
      });
      setLoading(false); // Stop loader
      return;
    }
    if (!csvFile) {
      Swal.fire({
        title: 'Datos faltantes',
        text: "Seleccione un fichero CSV",
        icon: 'error',
        confirmButtonText: 'Aceptar'
      });
      setLoading(false); // Stop loader
      return;
    }
    if (!selectedScenario && !newScenario) {
      Swal.fire({
        title: 'Datos faltantes',
        text: "Seleccione un escenario existente o ingrese un nuevo escenario",
        icon: 'error',
        confirmButtonText: 'Aceptar'
      });
      setLoading(false); // Stop loader
      return;
    }

    const formData = new FormData();
    formData.append('json_file', file);
    formData.append('csv_file', csvFile);
    formData.append('scenario', selectedScenario || newScenario);
    setLoading(true); // Start loader
    axiosInstance.post('/api/upload_combined', formData)
      .then(response => {
        Swal.fire({
          title: 'Flujo añadido',
          text: "El flujo se ha añadido correctamente",
          icon: 'success',
          confirmButtonText: 'Aceptar'
        });
      })
      .catch(error => {
        console.error('Error during upload:', error);
        Swal.fire({
          title: 'Error',
          text: "Ha habido un error durante la subida del flujo",
          icon: 'error',
          confirmButtonText: 'Aceptar'
        });
      })
      .finally(() => {
        setLoading(false); // Stop loader
      });
  };

  const handleDeleteFlow = () => {
    if (!selectedFlow) {
      Swal.fire({
        title: 'Flujo no seleccionado',
        text: "Seleccione un flujo para eliminar",
        icon: 'error',
        confirmButtonText: 'Aceptar'
      });
      return;
    }
    setLoading(true);
    axiosInstance.post('/api/delete_flow', { flow_id: selectedFlow })
      .then(response => {
        Swal.fire({
          title: 'Flujo eliminado',
          text: "Flujo eliminado correctamente",
          icon: 'success',
          confirmButtonText: 'Aceptar'
        });
        setFlows(flows.filter(flow => flow.id !== selectedFlow));
        if (selectedScenario) {
          fetchFlows(selectedScenario);
        }
        setSelectedFlow('');
      })
      .catch(error => {
        console.error('Error during delete:', error);
        Swal.fire({
          title: 'Error',
          text: "Ha habido un error durante la eliminación del flujo",
          icon: 'error',
          confirmButtonText: 'Aceptar'
        });
      }).finally(() => {
        setLoading(false); // Stop loader
      });
  };

  return (
    <div>
      <div className="navigation-bar">
        <NavigationBar />
      </div>
      <div className="admin">
        <h2>Admin View</h2>

        <div className="section">
          <h3>Añadir Flujo</h3>
          <form onSubmit={handleUpload} encType="multipart/form-data">
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
                  <option key={scenario.name} value={scenario.name}>{scenario.name}</option>
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

            <button type="submit">Añadir Flujo</button>
          </form>
        </div>

        {loading && (
          <Segment>
              <Loader>Cargando</Loader>
          </Segment>
        )}

        <div className="section">
          <h3>Eliminar Flujo</h3>
          <div className="flow-selection">
            <label htmlFor="flowSelect">Seleccione un flujo:</label>
            <select id="flowSelect" onChange={handleFlowChange}>
              <option value="">Seleccione un flujo</option>
              {flows.map(flow => (
                <option key={flow.id} value={flow.id}>{flow.name}</option>
              ))}
            </select>
            <button onClick={handleDeleteFlow}>Eliminar Flujo</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminView;





