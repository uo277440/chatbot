import React from 'react';
import HelloWorld from './HelloWorld';
import { AuthProvider } from './AuthContext';
import Chatbot from './Chatbot';
import Login from './Login';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
function App() {
  return (
    <AuthProvider>
      <Router>
          <Routes>
            <Route path='/' element={<Login />} />
            <Route path='/chatbot' element={<Chatbot />} />
          </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
