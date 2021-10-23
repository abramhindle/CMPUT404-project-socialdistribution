import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../UserContext";
import authorService from "../services/author";
import cookies from "js-cookies";

const Navbar = () => {
  const { user, setUser } = useContext(UserContext);
  return (
    <div>
      <Link to="/"> Home </Link>
      <Link to="/friends"> Friends </Link>
      <Link to="/myposts"> My Posts </Link>
      <Link to="/submit"> Submit </Link>
      { !user.id ? 
        <>
          <Link to="/login"> Login </Link>
          <Link to="/register"> Register </Link>
        </>
        :
        <>
          <div>{user.displayName}</div>
          <Link to="/profile">Profile</Link>
          <div onClick={() => { setUser(""); authorService.logout(cookies.getItem("csrftoken")) }}>Logout</div>
        </>
      }
    </div>
  )
}

export default Navbar;