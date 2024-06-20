import React from 'react';
import '../css/NotFound.css';

const NotFound = () => {
  return (
    <div className="not-found-container">
      <h1 className="not-found-title">404</h1>
      <p className="not-found-message">La página que está solicitando no existe</p>
      <div className="not-found-home">
        <a href="/">Volver a la página principal</a>
      </div>
    </div>
  );
};

export default NotFound;
