import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Outlet } from 'react-router-dom';

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © Social Distribution ' + new Date().getFullYear()}
    </Typography>
  );
}

const theme = createTheme();

export default function BaseTemplate() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container component="main" sx={{ paddingTop: 0, paddingBottom: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', minHeight: '100vh'}}>
        <Outlet />
        <Copyright sx={{marginTop: "100px" }} />
      </Container>
    </ThemeProvider>
  );
}