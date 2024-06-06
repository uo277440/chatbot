import '../css/Login.css';
import React, { useState, useEffect, useContext,useMemo } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import NavigationBar from '../NavigationBar';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import AuthContext from './AuthContext';
import logo from '../assets/logo.png'; // Import the logo image

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;



function Login() {
  const client = useMemo(() => axios.create({
    baseURL: 'http://localhost:8000',
    withCredentials: true
  }), []);
  const { currentUser, setCurrentUser } = useContext(AuthContext);
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    console.log('login')
    client.get("/api/user")
      .then(function (res) {
        setCurrentUser(res.data.user);
      })
      .catch(function (error) {
        setCurrentUser(null);
      });
  }, [setCurrentUser]);

  useEffect(() => {
    if (currentUser) {
      const user = currentUser;
      if (user.is_superuser) {
        navigate('/admin');
      } else {
        navigate('/menu');
      }
    }
  }, [currentUser, navigate]);

  function updateFormBtn() {
    setRegistrationToggle(!registrationToggle);
  }

  function handleSubmit(e) {
    e.preventDefault();
    if (registrationToggle) {
      submitRegistration();
    } else {
      submitLogin();
    }
  }

  function submitRegistration() {
    client.post(
      "/api/register",
      {
        email: email,
        username: username,
        password: password
      }
    ).then(function (res) {
      submitLogin();
    })
    .catch(error => {
      if (error.response) {
        console.log('Código de estado HTTP: ' + error.response.status);
        Swal.fire({
          title: 'Error',
          text: error.response.data.message,
          icon: 'error',
          confirmButtonText: 'Aceptar'
      });
      } else if (error.request) {
        console.error('No se recibió ninguna respuesta del servidor:', error.request);
      } else {
        console.error('Error al configurar la solicitud:', error.message);
      }
    });
  }

  function submitLogin() {
    client.post(
      "/api/login",
      {
        email: email,
        password: password
      }
    ).then(function (res) {
      const user = res.data.user;
      setCurrentUser(user);
      if (user.is_superuser) {
        navigate('/admin');
      } else {
        navigate('/menu');
      }
    })
    .catch(error => {
      if (error.response) {
        console.log('Código de estado HTTP: ' + error.response.status);
        Swal.fire({
          title: 'Error',
          text: error.response.data.message,
          icon: 'error',
          confirmButtonText: 'Aceptar'
      });
      } else if (error.request) {
        console.error('No se recibió ninguna respuesta del servidor:', error.request);
      } else {
        console.error('Error al configurar la solicitud:', error.message);
      }
    });
  }

  function handleLogout(e) {
    e.preventDefault();
    client.post(
      "/api/logout",
      { withCredentials: true }
    ).then(function (res) {
      setCurrentUser(null);
      navigate('/');
    });
  }

  return (
    <div>
      <NavigationBar
        currentUser={currentUser}
        handleLogout={handleLogout}
        registrationToggle={registrationToggle}
        updateFormBtn={updateFormBtn}
      />
      <Container className="login">
        <div className="login-content">
          <img src={logo} alt="App Logo" className="login-logo" />
          {renderLoginForm()}
        </div>
      </Container>
    </div>
  );

  function renderLoginForm() {
    return (
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Correo</Form.Label>
          <Form.Control type="email" placeholder="Introduce correo" value={email} onChange={e => setEmail(e.target.value)} />
          <Form.Text className="text-muted">
            Nunca compartiremos su contraseña con nadie.
          </Form.Text>
        </Form.Group>
        {registrationToggle && (
          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Usuario</Form.Label>
            <Form.Control type="text" placeholder="Introduce usuario" value={username} onChange={e => setUsername(e.target.value)} />
          </Form.Group>
        )}
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Contraseña</Form.Label>
          <Form.Control type="password" placeholder="Contraseña" value={password} onChange={e => setPassword(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Iniciar sesión
        </Button>
      </Form>
    );
  }
}

export default Login;


