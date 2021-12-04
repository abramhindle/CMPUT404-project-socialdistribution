import React, { useContext } from "react";
import { Link } from "react-router-dom";
import { useHistory } from 'react-router';
import { UserContext } from "../UserContext";
import authorService from "../services/author";
import cookies from "js-cookies";
import "./components.css"

const Navbar = () => {
  const { user, setUser } = useContext(UserContext);
  const history = useHistory();
  const logoutCurrentUser = () => {
    setUser({
      username: null,
      author: {
        authorID: null,
        displayName: null,
        host: null,
        github: null,
        profileImage: null,
      }
    });
    authorService.logout(cookies.getItem('csrftoken'));
    cookies.removeItem('csrftoken')
    cookies.removeItem('sessionid')
    localStorage.removeItem("authorID");
    localStorage.removeItem("username");
    history.push("/")
  }

  return (
    <div className='navbarContainer'>
      <text id="brand"> Socialisolation&nbsp;&nbsp;&nbsp;&nbsp; </text>
      
      {!user?.username ? (
        <>
          <Link to='/'> Login </Link>
          <Link to='/register'> Register </Link>
        </>
      ) : (
        <>
          <Link to='/'> Home </Link>
          <Link to='/friends'> Friends </Link>
          <Link to={`/author/${user.author.authorID}/posts`}> My Posts </Link>
          <Link to='/submit'> Submit </Link>
          <Link to='/browse'> Browse </Link>
          <div className='navbarAuthorname'>{user.author.displayName}</div>
          <Link to={`/author/${user.author.authorID}`} className='profileLink'>
            Profile
          </Link>
          <div
            className='navbarLogout'
            onClick={logoutCurrentUser}
          >
            Logout
          </div>
        </>
      )}
    </div>
  );
}

export default Navbar;