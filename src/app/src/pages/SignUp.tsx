import TextField, { TextFieldProps } from '@mui/material/TextField';
import LoadingButton, { LoadingButtonProps } from "@mui/lab/LoadingButton";
import { styled as Styled } from "@mui/material/styles";
import { useState } from "react";
import api from "../api/api";
import Author from "../api/models/Author";

const validate = (
  props: "email" | "password" | "displayName",
  item: string
) => {
  if (props === "email") {
    return !!item
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
  }

  if (props === "displayName") {
    return true;
  }

  if (props === "password") {
    return !!item;
  }

  return false;
};

const ColorButton = Styled(LoadingButton)<LoadingButtonProps>(({ theme }) => ({
  color: theme.palette.getContrastText("#e6c9a8"),
  padding: "10px",
  marginTop: "2%",
  backgroundColor: "#e6c9a8",
  "&:hover": {
    backgroundColor: "#D4AF85",
  },
}));

const TextFieldCustom = Styled(TextField)<TextFieldProps>(({ theme }) => ({
  color: theme.palette.getContrastText("#fbf8f0"),
  height: "50px",
  marginTop: "3%",
  "& .Mui-focused": {
    color: "black",
  },
  backgroundColor: "white",
  "&:hover": {
    backgroundColor: "#fbf8f0",
  },
}));

interface Props {
  setCurrentUser: React.Dispatch<React.SetStateAction<Author | undefined>>;
}

export default function SignUp({ setCurrentUser }: Props) {
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [validEmail, setValidEmail] = useState(true);
  const [validPassword, setValidPassword] = useState(true);
  const [validDisplayName, setValidDisplayName] = useState(true);
  const [isSigningUp, setIsSigningUp] = useState(false);

  const handleClick = () => {
    setValidEmail(validate("email", email));
    setValidDisplayName(validate("displayName", displayName));
    setValidPassword(validate("password", password));

    if (validEmail && validDisplayName && validPassword) {
      setIsSigningUp(true);
      api
        .register(email, password, displayName)
        .then((author) => setCurrentUser(author))
        .catch((error) => console.error(error))
        .finally(() => setIsSigningUp(false));
    }
  };
  const onChangeDisplayName = (event: any) => {
    setDisplayName(event?.target?.value);
  };
  const onChangeEmail = (event: any) => {
    setEmail(event?.target?.value);
  };
  const onChangePassword = (event: any) => {
    setPassword(event?.target?.value);
  };
  return (
    <>
      {validDisplayName ? (
        <TextFieldCustom
          id="standard-basic"
          color="primary"
          label="Display Name"
          variant="standard"
          onChange={onChangeDisplayName}
          helperText="Upto 16 characters."
        />
      ) : (
        <TextFieldCustom
          id="standard-error"
          color="primary"
          label="Display Name"
          variant="standard"
          onChange={onChangeDisplayName}
          helperText="Invalid display name"
        />
      )}
      {validEmail ? (
        <TextFieldCustom
          id="standard-basic"
          defaultValue={email}
          color="primary"
          label="Email"
          variant="standard"
          onChange={onChangeEmail}
        />
      ) : (
        <TextFieldCustom
          error
          id="outlined-error"
          defaultValue={email}
          label="Email"
          onChange={onChangeEmail}
          helperText="Incorrect email"
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
          helperText="Alphanumeric 16 characters."
        />
      ) : (
        <TextFieldCustom
          id="standard-error"
          label="Password"
          variant="standard"
          type="password"
          autoComplete="current-password"
          onChange={onChangePassword}
          helperText="Alphanumeric 16 characters!"
        />
      )}
      <ColorButton
        variant="contained"
        onClick={handleClick}
        loading={isSigningUp}
        disabled={isSigningUp}
      >
        Sign up
      </ColorButton>
    </>
  );
}
