import React from 'react';
import HelloWorld from './HelloWorld';
import { AuthProvider } from './AuthContext';
import Chatbot from './Chatbot';
import Login from './Login';
import Menu from './Menu';
import AdminView from './AdminView';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
import AdminMarks from './AdminMarks';
import Profile from './Profile';
function App() {
  return (
    <AuthProvider>
      <Router>
          <Routes>
            <Route path='/' element={<Login />} />
            <Route path='/chatbot' element={<Chatbot />} />
            <Route path='/admin' element={<AdminView />} />
            <Route path='/menu' element={<Menu />} />
            <Route path='/marks' element={<AdminMarks />} />
            <Route path='/profile' element={<Profile />} />
          </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
