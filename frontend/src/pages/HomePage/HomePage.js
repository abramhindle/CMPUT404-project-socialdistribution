import * as React from 'react';
import CreatePost from './createPost/CreatePost';
import ProfileSection from './profile/profileSection';
import FeedCard from './mainFeed/FeedCard';
import LogoutIcon from '@mui/icons-material/Logout';
import axios from 'axios';
import TabContext from '@mui/lab/TabContext';
import TabPanel from '@mui/lab/TabPanel';
import { useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { getInbox } from '../../Services/posts';
import { useState, useEffect } from 'react';
import { logout } from '../../redux/profileSlice';
import { set, findIndex, concat } from 'lodash/fp';
import { Alert, Snackbar, Drawer, Box, AppBar, Toolbar, Typography, Divider, Paper, IconButton, Grid, Button } from '@mui/material';
import NotificationCard from './notifications/NotificationCard';
import GithubFeedCard from './mainFeed/GithubFeedCard';
import {styled} from '@mui/system'
import { getNotifications } from '../../Services/notifications';
import { pushToInbox, setInbox } from '../../redux/inboxSlice';
import { getAllLikes } from '../../Services/likes';
import { getAuthorFromStorage, setAuthorInStorage  } from '../../LocalStorage/profile';
import { setInboxInStorage, getInboxFromStorage } from '../../LocalStorage/inbox';
import { getFollowers } from '../../Services/followers';
import PageviewRoundedIcon from '@mui/icons-material/PageviewRounded';
import ReceivedURLDialogs from './postSharing/receivedURL';

const drawerWidth = 400;

const Body = styled(Box)({ display: 'flex', paddingTop: "50px" });

const NavButton = styled(Button)({color: "white", textTransform: "none", fontSize:"1.2em"});

export default function HomePage() {

    /* Redux Dispatcher */
    const dispatch = useDispatch();

    /* State Hook For Tab Values */
    const [value, setValue] = React.useState('1');

    /* State Hook For Likes */
    const [allLikes, setAllLikes] = React.useState([]);

    /* State Hook For Displaying Alerts */
    const [openAlert, setOpenAlert] = useState({isOpen: false, message: "", severity: "error"})
    const alertSuccess = msg => setOpenAlert({isOpen: true, message: msg, severity: "success"})
    const alertError = msg => setOpenAlert({isOpen: true, message: msg, severity: "error"})
    const handleCloseAlert = () => setOpenAlert(set('isOpen', false, openAlert));

    /* A State Hook For Storing The Window Width */
    const [windowWidth, setWindowWidth] = useState(window.innerWidth)

    /* State Hook For Followers */
    const [followers, setFollowers] = useState([]);

    /* State Hook For Inbox */
    const [inbox, setInbox] = useState(getInboxFromStorage());
    
    /* Add A New Item To The Inbox */
    const addToFeed = (item) => {
        const newInbox = concat(inbox)(item).sort((a, b) => Date.parse(b.published) - Date.parse(a.published));
        setInbox(newInbox);
        setInboxInStorage(newInbox);
    }
    
    /* Remove An Item From The Inbox */
    const removeFromFeed = item => {
        const newInbox = inbox.filter( x => x.id !== item.id);
        setInbox(newInbox);
        setInboxInStorage(newInbox);
    };

    /* Update An Item In The Inbox */
    const updateFeed = (item) => {
        const index = findIndex(x => x.id === item.id)(inbox);
        const newInbox = inbox.map((x, i) => i === index ? item : x);
        setInbox(newInbox);
        setInboxInStorage(newInbox);
    }

    /* State Hook For User ID */
    const [author, setAuthor] = useState(getAuthorFromStorage());
    const editAuthor = (newGitHub, newProfileImage) => {
        const newAuthor = set("profileImage")(newProfileImage)(set("github")(newGitHub)(author));
        setAuthor(newAuthor);
        setAuthorInStorage(newAuthor);
    }

    /* State Hook For Notifications */
    const [notifications, setNotifications] = useState([])
    const removeNotification = (notification) => setNotifications(notifications.filter(x => x.id !== notification.id))

    /* State Hook For User*/
    const userObj = useSelector( state => state.profile );


    /* State Hook For GitHub */
    const [githubFeed, setGithubFeed] = useState([]);
    /* State Hook For ReceivedURL dialog*/
    const [openReceivedURL, setReceivedURLOpen] = React.useState(false);

    const handleReceivedURLClickOpen = () => {
        setReceivedURLOpen(true);
    };
    const handleReceivedURLClose = () => {
        setReceivedURLOpen(false);
    };

    /* We Use This To Listen To Changes In The Window Size */
    useEffect( () => { 
        const windowResizeCallback = () => { setWindowWidth(window.innerWidth) };
        window.addEventListener('resize', windowResizeCallback);
        return () => { window.removeEventListener('resize', windowResizeCallback) };
     });
    
    /* Hook For Navigating To The Home Page */
    const navigate = useNavigate();
    const goToLogin = () => navigate("/")

    /* Logout Functionality */
    const onLogout = () => {
      axios.post("/api/authors/logout/", {}, {headers: {"Authorization": "Token " + localStorage.getItem("token")}})
        .then( _ => {
            dispatch(logout());
            goToLogin();
         } )
        .catch( err => console.log(err) );
    }

    /* Get Inbox From Server 
    useEffect( () => {
        getInbox(author.url)
            .then( res => setInbox(res.data.items) )
            .catch( err => console.log(err) )
            .finally( () => console.log(inbox) )
    }, [] );
    */

    /* Get Notifications From Server  */
    useEffect( () => {
        getNotifications(author.url)
            .then( res => setNotifications(res.data.items) )
            .catch( err => console.log(err) )
            .finally( () => console.log(notifications) )
    }, [] );

    /* Get Followers From Server  */
    useEffect( () => {
        getFollowers(author.id)
            .then( res => console.log(res.data.items) )
            .catch( err => console.log(err) )
            .finally( () => console.log(followers) )
    }, [] );
    
    /* Get Github feed from Github API */
    useEffect( () => {
        const githubID = author.github.substring(author.github.lastIndexOf('/') + 1);
        console.log("https:/api.github.com/users/" + githubID + "/events/public")
        if (githubID.length !== 0) {
            axios.get("https:/api.github.com/users/" + githubID + "/events/public")
                .then( res => {
                    console.log(res.data)
                    setGithubFeed(res.data) 
                    console.log(githubFeed)
                })
                .catch( err => console.log(err) )
                .finally ( () => console.log(githubFeed) )
        }
        getAllLikes(userObj)
        .then( res => {
            setAllLikes(res.data.items)
        })
        .catch( err => console.log(err) )
        
    }, [] );

  return (
    <Body>
        <Snackbar
            sx={{width: "60%", pt:6}} spacing={2}
            anchorOrigin={{horizontal: "center", vertical: "top"}}
            open={openAlert.isOpen}
            autoHideDuration={2500}
            onClose={handleCloseAlert}>
            <Alert severity={openAlert.severity}>{openAlert.message}</Alert>
        </Snackbar>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar sx={{ flexWrap: 'wrap' }}>
                <Typography variant="h5" noWrap component="div"> Social Distribution </Typography>
                <span style={{float: "right", position: "absolute", right: 5}}>
                    <IconButton aria-label="delete" size="large" onClick={handleReceivedURLClickOpen}><PageviewRoundedIcon /></IconButton>
                    <NavButton onClick={() => setValue("1") }>Public</NavButton>
                    <NavButton onClick={() => setValue("2") }>Personal</NavButton>
                    <NavButton onClick={() => setValue("3") }>Management</NavButton>
                    <NavButton onClick={() => setValue("4") }>Notifications</NavButton>
                    <NavButton onClick={() => setValue("5") }>GitHub</NavButton>
                    <IconButton
                        onClick={onLogout}
                        id="account-icon"
                        size="large"
                        aria-label="account of current user"
                        aria-controls="menu-appbar"
                        aria-haspopup="true"
                        color="inherit" >
                        <LogoutIcon sx={{ fontSize: "36px" }}/>
                    </IconButton>
                </span>
            </Toolbar>
        </AppBar>
        <Drawer
            sx={{ width: drawerWidth, flexShrink: 0, '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box', }, }}
            variant="permanent"
            anchor="left" >
            <Toolbar />
            <Divider />
            <ProfileSection alertSuccess={alertSuccess} alertError={alertError} author={author} editAuthor={editAuthor} /> 
        </Drawer>
        <Box component="main" sx={{ flexGrow: 1, p: 0, marginTop: "15px", width: (windowWidth - drawerWidth) + "px"}}>
            <CreatePost alertSuccess={alertSuccess} alertError={alertError} addToFeed={addToFeed} />
            <Box sx={{ width: '100%', typography: 'body1' }}>
                <TabContext value={value}>
                    <TabPanel value="1" sx={{p:0}}>
                        {inbox.filter(post => post.visibility === "PUBLIC").map((post, index) => (
                            (<Grid item xs={12} key={index}> 
                                <FeedCard allLikes= {allLikes} profile = {userObj} post={post} isOwner={post.author.id === author.url} fullWidth={true} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} removeFromFeed={removeFromFeed} /> 
                            </Grid>)
                        ))}
                    </TabPanel>
                    <TabPanel value="2" sx={{p:0}}>
                        {inbox.filter(post => post.visibility !== "PUBLIC").map((post, index) => (
                            (<Grid item xs={12} key={index}> 
                                <FeedCard allLikes= {allLikes} post={post} isOwner={post.author.id === author.url} fullWidth={true} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} removeFromFeed={removeFromFeed} /> 
                            </Grid>)
                        ))}
                    </TabPanel>
                    <TabPanel value="3" sx={{p:0}}>
                        <Paper sx={{p:0}}>
                            {inbox.filter(post => post.author.id === author.url).map((post, index) => (
                                (<Grid item xs={12} key={index}> 
                                    <FeedCard allLikes= {allLikes} post={post} isOwner={post.author.id === author.url} fullWidth={true} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} removeFromFeed={removeFromFeed} /> 
                                </Grid>)
                            ))}
                        </Paper>
                    </TabPanel >
                    <TabPanel value="4" sx={{p:0}}>
                        <Paper sx={{p:0}}>
                            {notifications.map((notification, index) => (
                                (<Grid item xs={12} key={index}> 
                                    <NotificationCard notification={notification} removeNotification={removeNotification} fullWidth={true} alertError={alertError} alertSuccess={alertSuccess} /> 
                                </Grid>)
                            ))}
                        </Paper>
                    </TabPanel>
                    <TabPanel value="5" sx={{p:0}}>
                        {githubFeed?.map((event, index) => ( <Grid key={index} item xs={12}> <GithubFeedCard event={event} /> </Grid>))}
                    </TabPanel>
                </TabContext>
            </Box>
        </Box>
        <ReceivedURLDialogs open ={openReceivedURL} onClose={handleReceivedURLClose} alertSuccess={alertSuccess} alertError={alertError}></ReceivedURLDialogs>
    </Body>
    
  );
}