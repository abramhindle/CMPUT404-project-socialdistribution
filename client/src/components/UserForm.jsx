import React, { useState } from "react";
const UserForm = ({ onSubmit }) => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  return (
    <div>
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
      <button onClick={() => { onSubmit(username, password); setPassword(""); setUsername(""); }}>Submit</button>
    </div>
  )
};

export default UserForm;