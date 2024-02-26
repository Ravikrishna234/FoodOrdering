import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';

const MyOrders = () => {
  // Example orders data
  const orders = [
    {
      id: 1,
      date: '2024-02-10',
      totalPrice: 25.99,
      items: [
        { id: 1, name: 'Item 1', price: 10.99 },
        { id: 2, name: 'Item 2', price: 15.00 },
        { id: 3, name: 'Item 1', price: 10.99 },
        { id: 4, name: 'Item 2', price: 15.00 },
        { id: 5, name: 'Item 1', price: 10.99 },
        { id: 6, name: 'Item 2', price: 15.00 }
      ]
    },
    {
      id: 2,
      date: '2024-02-09',
      totalPrice: 18.50,
      items: [
        { id: 3, name: 'Item 3', price: 8.50 },
        { id: 4, name: 'Item 4', price: 10.00 }
      ]
    }
    // Add more orders as needed
  ];

  return (
    <Container className="overflow-auto">
      <h2 className="text-center mt-5 mb-4">My Orders</h2>
      {orders.map(order => (
        <Card key={order.id} className="mb-4">
          <Card.Header>
            <Row>
              <Col md={4}>
                <p className="fw-bold">Ordered Date: {order.date}</p>
              </Col>
              <Col md={4} className="text-center">
                <p className="fw-bold">Items</p>
              </Col>
              <Col md={4} className="text-end">
                <p className="fw-bold">Total Price: ${order.totalPrice.toFixed(2)}</p>
              </Col>
            </Row>
          </Card.Header>
          <Card.Body>
            {order.items.map(item => (
              <Row key={item.id} className="mb-2">
                <Col md={4}>
                  <p>{item.name}</p>
                </Col>
                <Col md={4} className="text-center">
                  <p>${item.price.toFixed(2)}</p>
                </Col>
                {/* You can add more details for each item here */}
              </Row>
            ))}
          </Card.Body>
        </Card>
      ))}
    </Container>
  );
};

export default MyOrders;
