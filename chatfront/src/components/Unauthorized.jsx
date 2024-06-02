import React from 'react';
import { Link } from 'react-router-dom';
import '../css/Unauthorized.css';

const Unauthorized = () => {
  return (
    <div className="unauthorized-container">
      <h1 className="unauthorized-heading">Unauthorized</h1>
      <p className="unauthorized-message">You do not have the required permissions to view this page.</p>
      <Link to="/" className="unauthorized-button">Go to Home</Link>
    </div>
  );
};

export default Unauthorized;

