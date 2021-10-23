import React from 'react';
import { useState } from 'react';
import authorService from '../../services/author';
import './styles.css';

const Register = () => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  const handleRegister = async (event) => {
    console.log('handling register look at me!!');
    const res = await authorService.register({ username, password });
    console.log(res);
  };

  return (
    <div className="registerContainer">
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
      <button onClick={handleRegister}>Submit</button>
    </div>
  );
};

export default Register;
