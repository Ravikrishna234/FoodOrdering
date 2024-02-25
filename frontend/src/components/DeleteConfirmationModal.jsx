import React from 'react';
import { Modal, Button } from 'react-bootstrap';

const DeleteConfirmationModal = ({ visible, item, onConfirm, onCancel }) => {
  return (
    <Modal show={visible} onHide={onCancel}>
      <Modal.Header closeButton>
        <Modal.Title>Confirm Delete</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        Are you sure you want to delete {item?.name}?
      </Modal.Body>
      <Modal.Footer>
        <Button variant="danger" onClick={onConfirm}>Delete</Button>
        <Button variant="secondary" onClick={onCancel}>Cancel</Button>
      </Modal.Footer>
    </Modal>
  );
};

export default DeleteConfirmationModal;
