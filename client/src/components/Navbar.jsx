import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { UserContext } from "../UserContext";
import authorService from "../services/author";
import cookies from "js-cookies";
import "./components.css"

const Navbar = () => {
  const { user, setUser } = useContext(UserContext);
  return (
    <div className='navbarContainer'>
      <Link to='/'> Home </Link>

      {!user.author.displayName ? (
        <>
          <Link to='/login'> Login </Link>
          <Link to='/register'> Register </Link>
        </>
      ) : (
        <>
          <Link to='/friends'> Friends </Link>
          <Link to='/myposts'> My Posts </Link>
          <Link to='/submit'> Submit </Link>
          <div className='navbarAuthorname'>{user.author.displayName}</div>
          <Link to='/profile' className='profileLink'>
            Profile
          </Link>
          <div
            className='navbarLogout'
            onClick={() => {
              setUser('');
              authorService.logout(cookies.getItem('csrftoken'));
            }}
          >
            Logout
          </div>
        </>
      )}
    </div>
  );
}

export default Navbar;