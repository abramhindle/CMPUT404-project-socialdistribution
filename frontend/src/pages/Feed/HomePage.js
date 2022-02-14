import * as React from 'react';
import Box from '@mui/material/Box';
import Drawer from '@mui/material/Drawer';
import CssBaseline from '@mui/material/CssBaseline';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import InboxSection from './InboxSection';
import CreatePost from './createPost';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import ProfileSection from './profileSection';

const drawerWidth = 250;

export default function HomePage() {
  return (
    <Paper sx={{marginTop: "8%", borderRadius: "10px"}}>
    <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div"> Social Distribution </Typography>
        </Toolbar>
      </AppBar>
      {/* <Drawer
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
        <List>
          {['Inbox', 'Starred', 'Send email', 'Drafts'].map((text, index) => (
            <ListItem button key={text}>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
        <Divider />
        <List>
          {['All mail', 'Trash', 'Spam'].map((text, index) => (
            <ListItem button key={text}>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
        </List>
      </Drawer> */}
      <Grid container spacing={0}>
            {/* <Grid item xs={12}> */}
              {/* <Paper sx={{ pl: 2, mt: 1, pt:2, display: 'flex', flexDirection: 'column', evaluation: 3, border: '2px solid lightgrey', boxShadow: 1, borderRadius: 1 }}> */}
                  {/* <Box>
                    <InboxSection >
                    </InboxSection>
                  </Box> */}
              {/* </Paper> */}
            {/* </Grid> */}
            <Grid item xs={12} md={5} lg={3}>
                <Box sx={{width: "100%", padding:"20px"}}>
                        <ProfileSection >
                        </ProfileSection>
                      </Box>
            </Grid>
            <Grid item xs={12} md={7} lg={9}>
            <Grid container direction={"column"}>
                <Box sx={{width: "100%", padding:"20px"}}>
                        <CreatePost></CreatePost>
                      </Box>
                        
                <Box sx={{width: "100%", paddingLeft:"20px", paddingRight:"20px", paddingBottom: "20px"}}>
                  <InboxSection >
                  </InboxSection>
                </Box>
                  
            </Grid>
            </Grid>
          </Grid>
    </Paper>
  );
}