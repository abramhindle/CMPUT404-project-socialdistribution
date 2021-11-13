import React from 'react';
import { useContext } from 'react';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import { useHistory } from 'react-router';
import './styles.css'
import UserForm from '../../components/UserForm';
const Login = () => {
  const { user, setUser } = useContext(UserContext);

  const history = useHistory();

  const handleLogin = async (username, password) => {
    try {
      const response = await authorService.login({ username, password });
      console.log(response.data);
      setUser({
        username: username,
        author: {
          authorID: response.data.id.split('/').at(-1),
          displayName: response.data.displayName,
          profileImage: response.data.profileImage,
          host: null,
          github: response.data.github,
        },
      });
      console.log(user);
      history.push('/');
      localStorage.setItem("authorID", response.data.id.split("/").at(-1));
      localStorage.setItem("username", username);
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className="loginContainer">
      <h3 className="loginHeader">Log In </h3>
      <UserForm onSubmit={handleLogin} />
    </div>
  );
};

export default Login;
