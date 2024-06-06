import React from 'react';
import { Link } from 'react-router-dom';
import '../css/Unauthorized.css';

const Unauthorized = () => {
  return (
    <div className="unauthorized-container">
      <h1 className="unauthorized-heading">Acceso Denegado</h1>
      <p className="unauthorized-message">No tienes permiso para acceder a esta página.</p>
      <Link to="/" className="unauthorized-button">Volver al menú</Link>
    </div>
  );
};

export default Unauthorized;

