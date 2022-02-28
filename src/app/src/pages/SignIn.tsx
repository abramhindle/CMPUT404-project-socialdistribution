import TextField, { TextFieldProps } from '@mui/material/TextField';
import Button, { ButtonProps } from '@mui/material/Button';
import { styled as Styled } from '@mui/material/styles';
import { useState } from 'react';

const validate = (props: 'email' | 'password' | 'username', item: string) => {
  if (props === 'username') {
    if (item.length > 16) return false;
    // fetch from database
    return true;
  }

  if (props === 'password') {
    if (item.length > 16) return false;
    // fetch from database
    return true;
  }
};

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
  const [validUsername, setValidUsername] = useState(true);
  const [validPassword, setValidPassword] = useState(true);

  const handleClick = () => {
    validate('username', username) ? setValidUsername(true) : setValidUsername(false);
    validate('password', password) ? setValidPassword(true) : setValidPassword(false);
    // eslint-disable-next-line @typescript-eslint/no-unused-expressions
    validUsername && validPassword ? localStorage.setItem('user', username) : null;
    //Discuss this^
  };
  const onChangeUsername = (event: any) => {
    setUsername(event?.target?.value);
  };
  const onChangePassword = (event: any) => {
    setPassword(event?.target?.value);
  };
  return (
    <>
      {validUsername ? (
        <TextFieldCustom
          id="standard-basic"
          color="primary"
          label="Username"
          variant="standard"
          onChange={onChangeUsername}
        />
      ) : (
        <TextFieldCustom
          id="standard-error"
          color="primary"
          label="Username"
          variant="standard"
          onChange={onChangeUsername}
          helperText="Incorrect username."
        />
      )}
      {validPassword ? (
        <TextFieldCustom
          id="standard-basic"
          label="Password"
          variant="standard"
          type="password"
          autoComplete="current-password"
          onChange={onChangePassword}
        />
      ) : (
        <TextFieldCustom
          id="standard-error"
          label="Password"
          variant="standard"
          type="password"
          autoComplete="current-password"
          onChange={onChangePassword}
          helperText="Incorrect password."
        />
      )}
      <ColorButton variant="contained" onClick={handleClick}>
        Sign in
      </ColorButton>
    </>
  );
}
