import React, { useState } from 'react';

const Home = () => {
  // Dummy data for McDonald's menu

  // Dummy data for restaurant selection dropdown
  const restaurantData = [
    { name: 'McDonald\'s', menu: [
      { type: 'Burgers', items: [
        { name: 'Big Mac', price: 5.99, veg: false },
        { name: 'Quarter Pounder', price: 6.49, veg: false },
        { name: 'Cheeseburger', price: 3.99, veg: false }
      ]},
      { type: 'Fries', items: [
        { name: 'French Fries', price: 2.99, veg: true },
        { name: 'Waffle Fries', price: 3.49, veg: true },
        { name: 'Curly Fries', price: 3.49, veg: true }
      ]},
      { type: 'Drinks', items: [
        { name: 'Coca-Cola', price: 1.99, veg: true },
        { name: 'Sprite', price: 1.99, veg: true },
        { name: 'Fanta', price: 1.99, veg: true }
      ]}
    ] },
    { name: 'Burger King', menu: [
      { type: 'Burgers', items: [
          { name: 'Whopper', price: 6.99, veg: false },
          { name: 'Bacon King', price: 7.49, veg: false },
          { name: 'Impossible Whopper', price: 6.99, veg: true }
      ]},
      { type: 'Fries', items: [
          { name: 'French Fries', price: 2.99, veg: true },
          { name: 'Onion Rings', price: 3.49, veg: true }
      ]},
      { type: 'Drinks', items: [
          { name: 'Coca-Cola', price: 1.99, veg: true },
          { name: 'Dr. Pepper', price: 1.99, veg: true }
      ]}
    ] },
    { name: 'KFC', menu: [
      { type: 'Chicken', items: [
          { name: 'Original Recipe Chicken', price: 5.99, veg: false },
          { name: 'Extra Crispy Chicken', price: 6.49, veg: false }
      ]},
      { type: 'Sides', items: [
          { name: 'Mashed Potatoes', price: 2.99, veg: true },
          { name: 'Cole Slaw', price: 2.49, veg: true }
      ]},
      { type: 'Drinks', items: [
          { name: 'Pepsi', price: 1.99, veg: true },
          { name: 'Mountain Dew', price: 1.99, veg: true }
      ]}
    ] }
  ];

  // State for filtering and sorting
  const [filter, setFilter] = useState('all'); // 'all', 'veg', 'nonveg', 'Burgers', 'Fries', 'Drinks'
  const [sortBy, setSortBy] = useState('price'); // 'price'
  const [showDropdown, setShowDropdown] = useState(false);
  const [selectedRestaurant, setSelectedRestaurant] = useState(restaurantData[0]);

  // Filter menu items based on selected filter
  const filteredMenu = selectedRestaurant.menu.map(section => ({
    type: section.type,
    items: section.items.filter(item => {
      if (filter === 'all') return true;
      if (filter === 'veg' && item.veg) return true;
      if (filter === 'nonveg' && !item.veg) return true;
      return item.name === filter;
    })
  }));

  // Sort menu items based on selected sorting
  filteredMenu.forEach(section => {
    section.items.sort((a, b) => {
      if (sortBy === 'price') return a.price - b.price;
      return 0;
    });
  });

  // Handler for adding item to cart
  const handleAddToCart = (item) => {
    console.log('Added to cart:', item);
    // Add your logic here to add item to cart
  };

  return (
    <div className="container mt-5 pb-5">
      {/* Filter, sort buttons, and restaurant selection dropdown */}
      <div className="d-flex justify-content-between mb-4">
        {/* Filter and sort buttons */}
        <div>
        <div className="mb-4">
        <button className={`btn btn-outline-primary me-2 ${filter === 'all' ? 'active' : ''}`} onClick={() => setFilter('all')}>All</button>
        <button className={`btn btn-outline-primary me-2 ${filter === 'veg' ? 'active' : ''}`} onClick={() => setFilter('veg')}>Veg</button>
        <button className={`btn btn-outline-primary me-2 ${filter === 'nonveg' ? 'active' : ''}`} onClick={() => setFilter('nonveg')}>Non Veg</button>
        <button className={`btn btn-outline-primary ${sortBy === 'price' ? 'active' : ''}`} onClick={() => setSortBy('price')}>Sort by Price</button>
      </div>
        </div>
        {/* Restaurant selection dropdown */}
        <div className="dropdown">
          <button
            className="btn btn-secondary dropdown-toggle"
            type="button"
            id="dropdownMenuButton"
            onClick={() => setShowDropdown(!showDropdown)}
          >
            {selectedRestaurant.name} <span className="circle"></span>
          </button>
          <ul className={`dropdown-menu${showDropdown ? ' show' : ''}`} aria-labelledby="dropdownMenuButton">
            {restaurantData.map((restaurant, index) => (
              <li key={index}>
                <button
                  className={`dropdown-item${selectedRestaurant.name === restaurant.name ? ' active' : ''}`}
                  onClick={() => {
                    setSelectedRestaurant(restaurant);
                    setShowDropdown(false);
                  }}
                >
                  {restaurant.name} <span className="circle"></span>
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
      {/* Menu sections */}
      {filteredMenu.map((section, index) => (
        section.items.length !== 0 && (
        <div key={index} className="mb-5">
          <h3 className="text-center mb-3">{section.type}</h3>
          <div className="row row-cols-1 row-cols-md-3 g-4">
            {section.items.map((item, i) => (
              <div key={i} className="col">
                <div className="card h-100">
                  <div className="card-body">
                    <h5 className="card-title">{item.name}</h5>
                    <p className="card-text">Price: ${item.price}</p>
                    <p className="card-text">Type: {item.veg ? 'Veg' : 'Non Veg'}</p>
                    <button className="btn btn-primary" onClick={() => handleAddToCart(item)}>Add to Cart</button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        )
      ))}
    </div>
  );
};

export default Home;
