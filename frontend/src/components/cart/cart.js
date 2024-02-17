import React, { useState, useEffect } from 'react';
import { BsPlus, BsDash, BsTrash } from 'react-icons/bs';
import { useNavigate } from 'react-router-dom';

function Cart() {
  const navigate = useNavigate();

  const [cartItems, setCartItems] = useState([]);

  // Example cart items data
  const exampleCartItems = [
    { _id: "item_id1", name: "Big Mac", price: 5.99, quantity: 1, image: "https://via.placeholder.com/150" },
    { _id: "item_id2", name: "Quarter Pounder", price: 6.49, quantity: 1, image: "https://via.placeholder.com/150" }
    // Add more items as needed
  ];

  useEffect(() => {
    // Fetch cart items from backend or set from local storage
    // For this example, setting example cart items
    setCartItems(exampleCartItems);
  }, []);

  // Calculate total price
  const totalPrice = cartItems.reduce((acc, item) => acc + item.price * item.quantity, 0);

  const handlePlaceOrder = () => {
    // Navigate to Checkout component and pass total price as prop
    navigate('/checkout', {state: { totalPrice }});

    // history.push('/checkout', { totalAmount: totalPrice });
  };

  const handleIncreaseQuantity = (itemId) => {
    setCartItems(prevItems =>
      prevItems.map(item =>
        item._id === itemId ? { ...item, quantity: item.quantity + 1 } : item
      )
    );
  };

  const handleDecreaseQuantity = (itemId) => {
    setCartItems(prevItems =>
      prevItems.map(item =>
        item._id === itemId && item.quantity > 1 ? { ...item, quantity: item.quantity - 1 } : item
      )
    );
  };

  const handleDeleteItem = (itemId) => {
    setCartItems(prevItems =>
      prevItems.filter(item => item._id !== itemId)
    );
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4">Cart</h2>
      {cartItems.map(item => (
        <div key={item._id} className="row border rounded mb-3 p-2 align-items-center">
          <div className="col-2">
            <img src={item.image} className="img-fluid" alt={item.name} />
          </div>
          <div className="col-4">
            <h5>{item.name}</h5>
            <p>Price: ${item.price}</p>
          </div>
          <div className="col-3 d-flex align-items-center">
            <button className="btn btn-outline-secondary me-2" onClick={() => handleDecreaseQuantity(item._id)}><BsDash /></button>
            <span>{item.quantity}</span>
            <button className="btn btn-outline-secondary ms-2" onClick={() => handleIncreaseQuantity(item._id)}><BsPlus /></button>
          </div>
          <div className="col-3 d-flex align-items-center justify-content-end">
            <button className="btn btn-danger me-2" onClick={() => handleDeleteItem(item._id)}><BsTrash /></button>
            <p>Total: ${item.price * item.quantity}</p>
          </div>
        </div>
      ))}
      <p className="mt-3">Total Price: ${totalPrice.toFixed(2)}</p>
      <button className="btn btn-primary" onClick={handlePlaceOrder}>Place Order</button>
    </div>
  );
}

export default Cart;
