import TextField, { TextFieldProps } from '@mui/material/TextField';
import Button, { ButtonProps } from '@mui/material/Button';
import { styled as Styled } from '@mui/material/styles';
import { useState } from 'react';

interface User {
  email: string;
  username: string;
  password: string;
}

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

export default function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleClick = () => {
    const user: User = {
      username: username,
      email: email,
      password: password,
    };
    console.log(username, password);
    localStorage.setItem('user', JSON.stringify(user));
    //Discuss this^
  };
  const onChangeUsername = (event: any) => {
    setUsername(event?.target?.value);
  };
  const onChangeEmail = (event: any) => {
    setEmail(event?.target?.value);
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
        color="primary"
        label="Email"
        variant="standard"
        onChange={onChangeEmail}
      />
      <TextFieldCustom
        id="standard-basic"
        label="Password"
        variant="standard"
        type="password"
        autoComplete="current-password"
        onChange={onChangePassword}
      />
      <ColorButton variant="contained" onClick={handleClick}>
        Sign up
      </ColorButton>
    </>
  );
}
