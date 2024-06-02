import React from 'react';
import { Navigate } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from './components/AuthContext';

const ProtectedRoute = ({ children, requireSuperuser }) => {
  const { currentUser } = useContext(AuthContext);

  if (!currentUser) {
    return <Navigate to="/" replace />;
  }

  if (requireSuperuser && !currentUser.is_superuser) {
    return <Navigate to="/unauthorized" replace />; // Redirigir a una página de no autorizado si no es superusuario
  }

  return children;
};

export default ProtectedRoute;
