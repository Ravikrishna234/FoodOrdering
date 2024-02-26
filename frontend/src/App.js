import React, { Suspense } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';

const Home = React.lazy(() => import('./components/Home/Home'));
const Register = React.lazy(() => import('./components/account/register/Register'));
const Login = React.lazy(() => import('./components/account/login/login'));
const Cart = React.lazy(() => import('./components/cart/cart'));
const Checkout = React.lazy(() => import('./components/Checkout/Checkout'));

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <Suspense fallback={<div>Loading...</div>}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path='/login' element={<Login />} />
          <Route path='/register' element={<Register />} />
          <Route path='/cart' element={<Cart />} />
          <Route path='/checkout' element={<Checkout />} />
        </Routes>
        </Suspense>
        <Footer />
      </div>
    </Router>
  );
};


export default App;
