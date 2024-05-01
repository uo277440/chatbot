import React from 'react';
import HelloWorld from './HelloWorld';
import { AuthProvider } from './AuthContext';
import Chatbot from './Chatbot';
import Login from './Login';
import AdminView from './AdminView';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
function App() {
  return (
    <AuthProvider>
      <Router>
          <Routes>
            <Route path='/' element={<Login />} />
            <Route path='/chatbot' element={<Chatbot />} />
            <Route path='/admin' element={<AdminView />} />
          </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
