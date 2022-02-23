import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import CreatePost from './createPost/CreatePost';
import ProfileSection from './profile/profileSection';
import Paper from '@mui/material/Paper';
import FeedCard from './mainFeed/FeedCard';
import IconButton from '@mui/material/IconButton';
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';
import Grid from '@mui/material/Grid';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { getInbox } from '../../services/posts';
import { useState, useEffect } from 'react';
import { setInbox } from '../../redux/inboxSlice';
import { logout } from '../../redux/profileSlice';

const drawerWidth = 450;


export default function HomePage() {

    /* Redux Dispatcher */
    const dispatch = useDispatch();

    /* A State Hook For Storing The Window Width */
    const [windowWidth, setWindowWidth] = React.useState(window.innerWidth)

    /* We Use This To Listen To Changes In The Window Size */
    React.useEffect( () => { 
        const windowResizeCallback = () => { setWindowWidth(window.innerWidth) };
        window.addEventListener('resize', windowResizeCallback);
        return () => { window.removeEventListener('resize', windowResizeCallback) };
     });

    /* Hook For Navigating To The Home Page */
    const navigate = useNavigate();
    const goToLogin = () => navigate("/login/")

    /* Logout Functionality */
    const onLogout = () => {
      axios.post("/api/authors/logout/", {}, {headers: {"Authorization": "Token " + localStorage.getItem("token")}})
        .then( _ => {
            dispatch(logout());
            goToLogin();
         } )
        .catch( err => console.log(err) );
    }

    /* State Hook For Inbox */
    const inbox = useSelector( state => state.inbox.items );

    /* Get Inbox From Server */
    useEffect( () => {
        console.log(inbox);
        getInbox("dummy_data")
            .then( res => dispatch( setInbox(res) ) )
            .catch( err => console.log(err) )
            .finally( () => console.log(inbox) )
    }, [] );
    

  return (
    <Box sx={{ display: 'flex', paddingTop: "50px" }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar sx={{ flexWrap: 'wrap' }}>
            <Typography variant="h5" noWrap component="div"> Social Distribution </Typography>
            <IconButton
                onClick={onLogout}
                id="account-icon"
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                color="inherit"
                sx={{marginLeft: "auto"}} >
                <LogoutIcon sx={{ fontSize: "36px" }}/>
            </IconButton>
            </Toolbar>
            
        </AppBar>
        <Drawer
            sx={{ width: drawerWidth, flexShrink: 0, '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box', }, }}
            variant="permanent"
            anchor="left" >
        <Toolbar />
        <Divider />
        <ProfileSection /> 
        </Drawer>
            <Box component="main" sx={{ flexGrow: 1, p: 0, marginTop: "15px", width: (windowWidth - drawerWidth) + "px"}}>
                <CreatePost></CreatePost>
                <Paper sx={{p:0}}>
                {inbox.map((feedData) => (
                      <Grid item xs={12}>
                          <FeedCard feedData={feedData} fullWidth={true} />
                      </Grid>
                      ))}
                </Paper>
            </Box>
    </Box>
  );
}