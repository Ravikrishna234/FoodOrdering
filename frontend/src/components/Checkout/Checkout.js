import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Row, Col, Form, Button, Modal } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import './Checkout.css';

const Checkout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const totalAmount = location.state ? location.state.totalPrice : 0;
  const [formData, setFormData] = useState({
    nameOnCard: '',
    cardNumber: '',
    expiryDate: '',
    cvv: ''
  });

  const [showModal, setShowModal] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Your checkout logic goes here
    console.log(formData);
    setShowModal(true);
    setTimeout(() => {
        setShowModal(false); // Hide modal after 3 seconds
        navigate('/'); // Redirect to home page
      }, 3000);
  };

  return (
    <div>
      <Container>
        <Row className="justify-content-md-center mt-5">
          <Col md={6}>
            <h2 className="text-center mb-4">Checkout</h2>
            <Form onSubmit={handleSubmit}>
              <Form.Group controlId="formNameOnCard" className="mb-3">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Name on Card</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter name on card"
                  name="nameOnCard"
                  value={formData.nameOnCard}
                  onChange={handleChange}
                />
              </Form.Group>
              <Form.Group controlId="formCardNumber" className="mb-3">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Card Number</Form.Label>
                <Form.Control
                  type="text"
                  placeholder="Enter card number"
                  name="cardNumber"
                  value={formData.cardNumber}
                  onChange={handleChange}
                />
              </Form.Group>
              <Row className="mb-3">
                <Col>
                  <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Expiry Date</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="MM/YY"
                    name="expiryDate"
                    value={formData.expiryDate}
                    onChange={handleChange}
                  />
                </Col>
                <Col>
                  <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>CVV</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="CVV"
                    name="cvv"
                    value={formData.cvv}
                    onChange={handleChange}
                  />
                </Col>
              </Row>
              <Form.Group controlId="formTotalAmount" className="mb-4">
                <Form.Label style={{ fontSize: '18px', fontWeight: 'bold' }}>Total Amount</Form.Label>
                <Form.Control
                  type="text"
                  readOnly
                  value={`$${totalAmount}`}
                />
              </Form.Group>
              <Button variant="primary" type="submit" className="w-100 mb-3">
                Confirm Payment
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>

      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Order Placed Successfully!</Modal.Title>
        </Modal.Header>
        <Modal.Body className="text-center">
          <div className="tick-container">
            <div className="tick">&#10004;</div>
          </div>
        </Modal.Body>
      </Modal>
    </div>
  );
};

export default Checkout;
