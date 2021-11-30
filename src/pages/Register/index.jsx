import React from 'react';
import authorService from '../../services/author';
import './styles.css';
import UserForm from '../../components/UserForm';
import { useHistory } from 'react-router';

const Register = () => {
  const history = useHistory();
  const handleRegister = async (username, password) => {
    try {
      await authorService.register({ username, password });
      history.push("/");
    } catch (ex) {
      alert("Registration Unsuccessful");
    }
  };

  return (
    <div className='registerContainer'>
      <h3>Register </h3>
      <UserForm onSubmit={handleRegister} />
    </div>
  );
};

export default Register;
