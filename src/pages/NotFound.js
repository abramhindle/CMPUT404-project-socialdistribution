import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => (
  <div style={{display: "flex", height:"100vh", 
    flexDirection: "column", 
    alignItems: "center", justifyContent: "center"}}>
      <h1>404 - Not Found!</h1>
      <Link to="/">
        Go Home
      </Link>
  </div>
);

export default NotFound;