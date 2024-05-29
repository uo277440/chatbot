import React from 'react';
import { AuthProvider } from './AuthContext';
import Chatbot from './Chatbot';
import Login from './Login';
import Menu from './Menu';
import AdminView from './AdminView';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom';
import AdminMarks from './AdminMarks';
import Profile from './Profile';
import Forum from './Forum';
import NavigationBar from './NavigationBar';
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

