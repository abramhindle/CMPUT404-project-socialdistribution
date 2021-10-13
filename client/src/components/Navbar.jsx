import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div>
      <Link to="/"> Home </Link>
      <Link to="/friends"> Friends </Link>
      <Link to="/myposts"> My Posts </Link>
      <Link to="/submit"> Submit </Link>
    </div>
  )
}

export default Navbar;