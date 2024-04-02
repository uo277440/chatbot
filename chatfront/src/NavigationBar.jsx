// NavigationBar.jsx

import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

const NavigationBar = ({ currentUser, handleLogout, registrationToggle, updateFormBtn }) => {
  return (
    <Navbar bg="dark" variant="dark">
      <Container>
        <Navbar.Brand>Authentication App</Navbar.Brand>
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