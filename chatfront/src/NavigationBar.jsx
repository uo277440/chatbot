import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import AuthContext from './AuthContext';

const NavigationBar = ({ registrationToggle, updateFormBtn }) => {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true
  });

  const handleLogout = (e) => {
    e.preventDefault();
    axiosInstance.post("/api/logout")
      .then(res => {
        setCurrentUser(false);
        navigate('/');
      })
      .catch(error => {
        console.log('Error during logout:', error);
      });
  };

  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand>CHATBOT</Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
          <Navbar.Text>
            {currentUser ? (
              <form onSubmit={handleLogout}>
                <Button type="submit" variant="light">Log out</Button>
              </form>
            ) : (
              <Button id="form_btn" onClick={updateFormBtn} variant="light">{registrationToggle ? 'Log in' : 'Register'}</Button>
            )}
          </Navbar.Text>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;
