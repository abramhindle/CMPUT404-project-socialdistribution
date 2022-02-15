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
import Grid from '@mui/material/Grid';
import IconButton from '@mui/material/IconButton';
import LogoutIcon from '@mui/icons-material/Logout';

const drawerWidth = 350;

const feedData={

}

export default function HomePage() {

    const [windowWidth, setWindowWidth] = React.useState(window.innerWidth)

    React.useEffect( () => { window.addEventListener('resize', () => setWindowWidth(window.innerWidth) ) });

  return (
    <Box sx={{ display: 'flex', paddingTop: "50px" }}>
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
            <Toolbar sx={{ flexWrap: 'wrap' }}>
            <Typography variant="h6" noWrap component="div"> Social Distribution </Typography>
            <IconButton
                    id="account-icon"
                    size="large"
                    aria-label="account of current user"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    color="inherit"
                    sx={{marginLeft: "auto"}}
                    >
                    <LogoutIcon sx={{ fontSize: "36px" }}/>
                    </IconButton>
            </Toolbar>
            
        </AppBar>
        <Drawer
            sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
                width: drawerWidth,
                boxSizing: 'border-box',
            },
            }}
            variant="permanent"
            anchor="left"
        >
        <Toolbar />
        <Divider />
        <ProfileSection /> 
        </Drawer>
            <Box component="main" sx={{ flexGrow: 1, p: 0, marginTop: "15px", width: (windowWidth - drawerWidth) + "px"}}>
                <CreatePost></CreatePost>
                <Paper sx={{p:2}}>
                {/* {feedData.map((prizeData) => (
                      <Grid item xs={12}>
                          <FeedCard feedData={feedData} fullWidth={true} />
                      </Grid>
                      ))} */}
                  <FeedCard></FeedCard>
                  <FeedCard></FeedCard>
                  <FeedCard></FeedCard>
                </Paper>
            </Box>
    </Box>
  );
}