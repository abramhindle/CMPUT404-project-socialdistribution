import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Snackbar from '@mui/material/Snackbar';
import { Alert } from '@mui/material';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import { set } from 'lodash/fp';

export default function LoginPage() {

  const [openAlert, setOpenAlert] = React.useState({isOpen: false, message: "", severity: "error"})

  const showError = msg => setOpenAlert({isOpen: true, message: msg, severity: "error"})
  const handleCloseAlert = () => setOpenAlert(set('isOpen', false, openAlert));

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if (data.get("password") && data.get("displayName")) {
      axios.post("/api/authors/login/", data)
        .then((res) => {
            localStorage.setItem("jwtToken", res.data.token);
            localStorage.setItem("userID",res.data.id);
            handleClick(true);
            history.push("/homepage/");
        })
        .catch( err => showError(err.response.data.error) );
    } else {
      showError("Username And Password Required!")
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center", height: "100vh"}}>
      <Snackbar
        sx={{width: "60%", pt:6}} spacing={2}
        anchorOrigin={{horizontal: "center", vertical: "top"}}
        open={openAlert.isOpen}
        autoHideDuration={2500}
        onClose={handleCloseAlert}>
        <Alert severity={openAlert.severity}>{openAlert.message}</Alert>
      </Snackbar>
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', maxWidth: "400px" }} >
        <Typography component="h1" variant="h5">
          Sign In
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                name="displayName"
                required
                fullWidth
                id="displayName"
                label="Username"
                autoFocus
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="new-password"
              />
            </Grid>
          </Grid>
          <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }} > Sign In </Button>
          <Grid container justifyContent="center">
            <Grid item>
              <Link href="/register" variant="body2">
                New user? Create an account
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </div>
  );
}