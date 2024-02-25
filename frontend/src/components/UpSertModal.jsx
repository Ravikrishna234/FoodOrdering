import React, { useEffect, useState } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const UpSertModal = ({ visible, item, onSave, onCancel, isAdd }) => {
  const [editedItem, setEditedItem] = useState(null);

  // Initialize the editedItem state with the item prop when the component mounts
  useEffect(() => {
    setEditedItem(item);
  }, [item]); // Add item as a dependency to update the state when it changes

  // Function to handle form input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditedItem({ ...editedItem, [name]: value });
  };

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(editedItem);
  };

  return (
    <Modal show={visible} onHide={onCancel}>
      <Modal.Header closeButton>
        <Modal.Title>{isAdd ? ('Add') : ('Edit')} Item</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="editFormName">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              name="name"
              value={editedItem?.name || ''} 
              onChange={handleChange}
            />
          </Form.Group>
          <Form.Group controlId="editFormPrice">
            <Form.Label>Price</Form.Label>
            <Form.Control
              type="text"
              name="price"
              value={editedItem?.price || ''}
              onChange={handleChange}
            />
          </Form.Group>
          {/* Dropdown for selecting type */}
          <Form.Group controlId="editFormType">
            <Form.Label>Type</Form.Label>
            <Form.Control
              as="select"
              name="type"
              value={editedItem?.type || ''}
              onChange={handleChange}
            >
              <option value="Non-Veg">Non-Veg</option>
              <option value="Veg">Veg</option>
            </Form.Control>
          </Form.Group>
        </Form>
      </Modal.Body>
      {/* Fix styling issue */}
      <Modal.Footer>
        <Button variant="secondary" onClick={onCancel}>Cancel</Button>
        <Button variant="primary" type="submit" onClick={handleSubmit}>Save Changes</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default UpSertModal;
