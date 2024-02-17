import React, { useState } from 'react';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';

const Register = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [validated, setValidated] = useState(false);
  const [showError, setShowError] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    if (form.checkValidity() === false) {
      e.stopPropagation();
    } else {
      // Your registration logic goes here
      console.log(formData);
      setValidated(false);
      setShowError(false);
    }
    setValidated(true);
    setShowError(true);
  };

  return (
    <div style={{ height: 'calc(100vh - 56px)', overflowY: 'auto' }}>
      {/* 56px is the height of your Navbar */}
      <Container>
        <Row className="justify-content-md-center mt-5">
          <Col md={6}>
            <h2 className="text-center">Register</h2>
            <Form noValidate validated={validated} onSubmit={handleSubmit}>
              <Form.Group controlId="formFirstName" className="mb-3">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>First Name</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter first name"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleChange}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid first name.
                </Form.Control.Feedback>
              </Form.Group>
              <Form.Group controlId="formLastName" className="mb-3">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Last Name</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter last name"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleChange}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid last name.
                </Form.Control.Feedback>
              </Form.Group>
              <Form.Group controlId="formEmail" className="mb-3">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Email address</Form.Label>
                <Form.Control
                  type="email"
                  placeholder="Enter email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid email address.
                </Form.Control.Feedback>
              </Form.Group>
              <Form.Group controlId="formPassword" className="mb-3">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid password.
                </Form.Control.Feedback>
              </Form.Group>
              <Form.Group controlId="formConfirmPassword" className="mb-4">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Confirm Password</Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Confirm password"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
                <Form.Control.Feedback type="invalid">
                  Please provide a valid confirmation password.
                </Form.Control.Feedback>
              </Form.Group>
              {showError && (
                <Alert variant="danger" onClose={() => setShowError(false)} dismissible>
                  Please fix the errors before submitting the form.
                </Alert>
              )}
              <Button variant="primary" type="submit" className="w-100 mb-3">
                Register
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Register;
