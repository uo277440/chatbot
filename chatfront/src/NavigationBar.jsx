import React, { useContext, useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import Nav from 'react-bootstrap/Nav';
import AuthContext from './AuthContext';

const NavigationBar = ({ registrationToggle, updateFormBtn }) => {
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();
  
  const axiosInstance = axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true
  });

  useEffect(() => {
    if (currentUser) {
      axiosInstance.get('/api/user')
        .then(res => {
          setUserData(res.data.user);
        })
        .catch(error => {
          console.log('Error fetching user data:', error);
        });
    }
  }, [currentUser]);

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
          {currentUser ? (
            <>
              {userData && (
                <Nav>
                  {userData.is_superuser ? (
                    <>
                      <Nav.Link as={Link} to="/marks">Evaluador</Nav.Link>
                      <Nav.Link as={Link} to="/admin">Panel</Nav.Link>
                    </>
                  ) : (
                    <>
                      <Nav.Link as={Link} to="/menu">Menú</Nav.Link>
                      <Nav.Link as={Link} to="/chatbot">Chatbot</Nav.Link>
                      <Nav.Link as={Link} to="/profile">Perfil</Nav.Link>
                    </>
                  )}
                </Nav>
              )}
              <form onSubmit={handleLogout} className="ml-auto">
                <Button type="submit" variant="light">Log out</Button>
              </form>
            </>
          ) : (
            <Button id="form_btn" onClick={updateFormBtn} variant="light">{registrationToggle ? 'Log in' : 'Register'}</Button>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default NavigationBar;

