import TextField, { TextFieldProps } from '@mui/material/TextField';
import LoadingButton, { LoadingButtonProps } from "@mui/lab/LoadingButton";
import { styled as Styled } from "@mui/material/styles";
import { useState } from "react";
import api from "../api/api";
import Author from "../api/models/Author";

const validate = (props: "email" | "password", item: string) => {
  if (props === "email") {
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
  padding: "10px",
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

export default function SignIn({ setCurrentUser }: Props) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [validEmail, setValidEmail] = useState(true);
  const [validPassword, setValidPassword] = useState(true);
  const [isSigningIn, setIsSigningIn] = useState(false);

  const handleClick = () => {
    setValidEmail(validate("email", email));
    setValidPassword(validate("password", password));

    if (validEmail && validPassword) {
      setIsSigningIn(true);
      api
        .login(email, password)
        .then((user) => setCurrentUser(user))
        .catch((err) => console.log(err))
        .finally(() => setIsSigningIn(false));
    }
  };

  const onChangeEmail = (event: any) => {
    setEmail(event?.target?.value);
  };
  const onChangePassword = (event: any) => {
    setPassword(event?.target?.value);
  };

  return (
    <>
      {validEmail ? (
        <TextFieldCustom
          id="standard-basic"
          color="primary"
          label="Email"
          variant="standard"
          onChange={onChangeEmail}
        />
      ) : (
        <TextFieldCustom
          id="standard-error"
          color="primary"
          label="Username"
          variant="standard"
          onChange={onChangeEmail}
          helperText="Invalid email."
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
      <ColorButton
        variant="contained"
        onClick={handleClick}
        loading={isSigningIn}
        disabled={isSigningIn}
      >
        Sign in
      </ColorButton>
    </>
  );
}
