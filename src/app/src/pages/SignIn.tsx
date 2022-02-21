import styled from 'styled-components';
import TextField, { TextFieldProps } from '@mui/material/TextField';
import Button, { ButtonProps } from '@mui/material/Button';
import { makeStyles, styled as Styled } from '@mui/material/styles';
import { useState } from 'react';

const ColorButton = Styled(Button)<ButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#e6c9a8'),
  padding: '10px',
  marginTop: '2%',
  backgroundColor: '#e6c9a8',
  '&:hover': {
    backgroundColor: '#D4AF85',
  },
}));

const TextFieldCustom = Styled(TextField)<TextFieldProps>(({ theme }) => ({
  color: theme.palette.getContrastText('#fbf8f0'),
  height: '50px',
  padding: '10px',
  '& .Mui-focused': {
    color: 'black',
  },
  backgroundColor: 'white',
  '&:hover': {
    backgroundColor: '#fbf8f0',
  },
}));

export default function SignIn() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleClick = () => {
    console.log(username, password);
  };
  const onChangeUsername = (event: any) => {
    setUsername(event?.target?.value);
  };
  const onChangePassword = (event: any) => {
    setPassword(event?.target?.value);
  };
  return (
    <>
      <TextFieldCustom
        id="standard-basic"
        color="primary"
        label="Username"
        variant="standard"
        onChange={onChangeUsername}
      />
      <TextFieldCustom
        id="standard-basic"
        label="Password"
        variant="standard"
        onChange={onChangePassword}
      />
      <ColorButton variant="contained" onClick={handleClick}>
        Sign in
      </ColorButton>
    </>
  );
}
