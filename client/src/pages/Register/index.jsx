import React from 'react';
import authorService from '../../services/author';
import './styles.css';
import UserForm from '../../components/UserForm';
import { useHistory } from 'react-router';

const Register = () => {
  const history = useHistory();
  const handleRegister = async (username, password) => {
    try {
      const res = await authorService.register({ username, password });
      console.log(res);
      history.push("/");
    } catch (ex) {
      alert("Registration Unsuccessful");
    }
  };

  return (
    <div className='registerContainer'>
      <h3 className='registerHeader'>Register </h3>
      <UserForm onSubmit={handleRegister} />
    </div>
  );
};

export default Register;
