import React from 'react';
import { useState, useContext } from 'react';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import { useHistory } from 'react-router';
import './styles.css'
const Login = () => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  const { user, setUser } = useContext(UserContext);

  const history = useHistory();

  const handleLogin = async (event) => {
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
      setUsername('');
      setPassword('');
    }
  };

  return (
    <div className="loginContainer">
      <label>
        Username:
        <input
          type='username'
          onChange={(e) => {
            setUsername(e.target.value);
          }}
        ></input>
      </label>
      <label>
        Password:
        <input
          type='password'
          onChange={(e) => {
            setPassword(e.target.value);
          }}
        ></input>
      </label>
      <button onClick={handleLogin}>Submit</button>
    </div>
  );
};

export default Login;
