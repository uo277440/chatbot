import React, { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../css/Menu.css';
import NavigationBar from '../NavigationBar';

function Menu() {
    const [scenarios, setScenarios] = useState([]);
    const [flowsByScenario, setFlowsByScenario] = useState({});
    const navigate = useNavigate();
    const axiosInstance = useMemo(() => axios.create({
        baseURL: 'http://localhost:8000',
        withCredentials: true
    }), []);

    useEffect(() => {
        // Fetch existing scenarios and their flows when component mounts
        fetchScenariosAndFlows();
    }, []);

    const fetchScenariosAndFlows = async () => {
        try {
            const scenariosResponse = await axiosInstance.get('/api/scenarios');
            const scenarios = scenariosResponse.data.scenarios;
            setScenarios(scenarios);

            const flowsByScenario = {};
            await Promise.all(scenarios.map(async (scenario) => {
                const flowsResponse = await axiosInstance.get(`/api/flows/?scenery_id=${scenario.id}`);
                flowsByScenario[scenario.id] = flowsResponse.data.flows;
            }));
            setFlowsByScenario(flowsByScenario);
        } catch (error) {
            console.error('Error fetching scenarios and flows:', error);
        }
    };

    const handleFlowClick = (flowId) => {
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
            });
    };

    return (
        <div className="menu">
            <NavigationBar />
            <h1>Selecciona un escenario:</h1>
            <div className="scenario-container">
                {scenarios.map(scenario => (
                    <div key={scenario.id} className="scenario">
                        <h2>{scenario.name}</h2>
                        <ul className="flow-list">
                            {flowsByScenario[scenario.id]?.map(flow => (
                                <li key={flow.id} onClick={() => handleFlowClick(flow.id)}>
                                    {flow.name}
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default Menu;

