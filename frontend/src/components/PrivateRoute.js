import {React} from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element: Component, isAuthenticated, isAuthorized, ...rest }) => {
    

  return isAuthenticated ? (
    <Component />
  ) : (
    <Navigate to="/login" replace />
  );
};

export default PrivateRoute;
