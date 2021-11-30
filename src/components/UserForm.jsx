import React, { useState } from "react";
import {TextField, Button} from '@material-ui/core'
const UserForm = ({ onSubmit }) => {
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');

  return (
    <div className='userFormContainer'>
      <TextField
        label='Username'
        variant='outlined'
        size='small'
        onChange={(e) => {
          setUsername(e.target.value);
        }}
      />
      <br />
      <TextField
        label='Password'
        type='password'
        variant='outlined'
        size='small'
        onChange={(e) => {
          setPassword(e.target.value);
        }}
      />
      <br />
      <Button
        variant='contained'
        onClick={() => {
          onSubmit(username, password);
          setPassword('');
          setUsername('');
        }}
      >
        SUBMIT
      </Button>
    </div>
  );
};

export default UserForm;