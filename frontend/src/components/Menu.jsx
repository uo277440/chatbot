import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../css/Menu.css';
import NavigationBar from '../NavigationBar';
import { Dimmer, Loader } from 'semantic-ui-react';

function Menu() {
    const [scenarios, setScenarios] = useState([]);
    const [selectedScenario, setSelectedScenario] = useState(null);
    const [flows, setFlows] = useState([]);
    const [loading, setLoading] = useState(false); // Loader state
    const navigate = useNavigate();
    const axiosInstance = useMemo(() => axios.create({
        baseURL: '/choreo-apis/chatbottfg/backend/v1',
        withCredentials: true
    }), []);

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

    const fetchFlowsByScenario = (scenarioId) => {
        axiosInstance.get(`/api/flows/?scenery_id=${scenarioId}`)
            .then(response => {
                const flows = response.data.flows;
                setFlows(flows);
            })
            .catch(error => {
                console.error('Error fetching flows:', error);
            });
    };

    const handleScenarioHover = (scenario) => {
        setSelectedScenario(scenario);
        fetchFlowsByScenario(scenario.id);
    };

    const handleScenarioLeave = () => {
        setSelectedScenario(null);
        setFlows([]);
    };

    const handleFlowClick = (flowId) => {
        setLoading(true); // Start loader
        const currentFlowId = localStorage.getItem('currentFlowId');
        if (currentFlowId != null) {
            if (currentFlowId.toString() !== flowId.toString()) {
                localStorage.removeItem('chatMessages');
                localStorage.setItem('currentFlowId', flowId.toString());
                localStorage.setItem('showHelp', JSON.stringify(false));
                localStorage.setItem('first', JSON.stringify(true));
            }
        }
        axiosInstance.get(`/api/start_flow?flow_id=${flowId}`)
            .then(response => {
                navigate('/chatbot');
            })
            .catch(error => {
                console.error('Error al iniciar el flujo:', error);
            })
            .finally(() => {
                setLoading(false); // Stop loader
            });
    };

    return (
        <div className="menu">
            <NavigationBar />
            <h1>Selecciona un escenario:</h1>
            <div className="scenario-container">
                {scenarios.map(scenario => (
                    <div key={scenario.id} className="scenario"
                        onMouseEnter={() => handleScenarioHover(scenario)}
                        onMouseLeave={() => handleScenarioLeave()}>
                        <h2>{scenario.name}</h2>
                        {selectedScenario && selectedScenario.id === scenario.id &&
                            <ul className="flow-list">
                                {flows.map(flow => (
                                    <li key={flow.id} onClick={() => handleFlowClick(flow.id)}>
                                        {flow.name}
                                    </li>
                                ))}
                            </ul>
                        }
                    </div>
                ))}
            </div>
            {loading && (
                <Dimmer active>
                    <Loader>Cargando</Loader>
                </Dimmer>
            )}
        </div>
    );
}

export default Menu;

