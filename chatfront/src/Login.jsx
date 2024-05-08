// Login.jsx

import './Login.css';
import React, { useState, useEffect, useContext  } from 'react';
import axios from 'axios';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import NavigationBar from './NavigationBar';
import { useNavigate } from 'react-router-dom';
import AuthContext from './AuthContext';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const client = axios.create({
  baseURL: "http://localhost:8000"
});

function Login() {
  const { currentUser, setCurrentUser } = useContext(AuthContext)
  const [registrationToggle, setRegistrationToggle] = useState(false);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    client.get("/api/user")
      .then(function (res) {
        setCurrentUser(true);
      })
      .catch(function (error) {
        setCurrentUser(false);
      });
  }, []);

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
      navigate('/menu');
      setCurrentUser(true);
    });
  }

  function handleLogout(e) {
    e.preventDefault();
    client.post(
      "/api/logout",
      { withCredentials: true }
    ).then(function (res) {
      setCurrentUser(false);
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
      <Container className="center">
        {renderLoginForm()}
      </Container>
    </div>
  );

  function renderLoginForm() {
    return (
      <Form onSubmit={handleSubmit}>
        <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label>Email address</Form.Label>
          <Form.Control type="email" placeholder="Enter email" value={email} onChange={e => setEmail(e.target.value)} />
          <Form.Text className="text-muted">
            We'll never share your email with anyone else.
          </Form.Text>
        </Form.Group>
        {registrationToggle && (
          <Form.Group className="mb-3" controlId="formBasicUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control type="text" placeholder="Enter username" value={username} onChange={e => setUsername(e.target.value)} />
          </Form.Group>
        )}
        <Form.Group className="mb-3" controlId="formBasicPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        </Form.Group>
        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    );
  }
}

export default Login;
