import React, { useState } from "react";
const UserForm = ({ onSubmit }) => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  return (
    <div className="userFormContainer">
      <label>
        Username
        <input
          type='username'
          onChange={(e) => {
            setUsername(e.target.value);
          }}
        ></input>
      </label>
      <label>
        Password 
        <input
          type='password'
          onChange={(e) => {
            setPassword(e.target.value);
          }}
        ></input>
      </label>
      <button className="userFormButton" onClick={() => { onSubmit(username, password); setPassword(""); setUsername(""); }}>SUBMIT</button>
    </div>
  )
};

export default UserForm;