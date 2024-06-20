import React from 'react';
import { AuthProvider } from './components/AuthContext';
import Chatbot from './components/Chatbot';
import Login from './components/Login';
import Menu from './components/Menu';
import AdminView from './components/AdminView';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import AdminMarks from './components/AdminMarks';
import Profile from './components/Profile';
import Forum from './components/Forum';
import ProtectedRoute from './ProtectedRoute';
import Unauthorized from './components/Unauthorized'; 
import NotFound from './components/NotFound';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <div className="background">
        <Router>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route
              path="/chatbot"
              element={
                <ProtectedRoute>
                  <Chatbot />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <ProtectedRoute requireSuperuser={true}>
                  <AdminView />
                </ProtectedRoute>
              }
            />
            <Route
              path="/menu"
              element={
                <ProtectedRoute>
                  <Menu />
                </ProtectedRoute>
              }
            />
            <Route
              path="/marks"
              element={
                <ProtectedRoute requireSuperuser={true}>
                  <AdminMarks />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/forumMessage"
              element={
                <ProtectedRoute>
                  <Forum />
                </ProtectedRoute>
              }
            />
            <Route path="/unauthorized" element={<Unauthorized />} /> {/* Ruta para no autorizado */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Router>
      </div>
    </AuthProvider>
  );
}

export default App;


