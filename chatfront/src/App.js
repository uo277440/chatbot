import React from 'react';
import { AuthProvider } from './components/AuthContext';
import Chatbot from './components/Chatbot';
import Login from './components/Login';
import Menu from './components/Menu';
import AdminView from './components/AdminView';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
import AdminMarks from './components/AdminMarks';
import Profile from './components/Profile';
import Forum from './components/Forum';
import './App.css';




function App() {
  return (
    <AuthProvider>
      <div className="background">
      <Router>
        <Routes>
          <Route path='/' element={<Login />} />
          <Route path='/chatbot' element={<Chatbot />} />
          <Route path='/admin' element={<AdminView />} />
          <Route path='/menu' element={<Menu />} />
          <Route path='/marks' element={<AdminMarks />} />
          <Route path='/profile' element={<Profile />} />
          <Route path='/forumMessage' element={<Forum />} />
        </Routes>
      </Router>
      </div>
    </AuthProvider>
  );
}

export default App;

