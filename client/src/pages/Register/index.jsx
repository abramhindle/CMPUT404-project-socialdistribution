import React from 'react';
import authorService from '../../services/author';
import './styles.css';
import UserForm from '../../components/UserForm';

const Register = () => {
  const handleRegister = async (username, password) => {
    const res = await authorService.register({ username, password });
    console.log(res);
  };

  return (
    <div className="registerContainer">
      <UserForm onSubmit={handleRegister} />
    </div>
  );
};

export default Register;
