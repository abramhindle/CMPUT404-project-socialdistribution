import * as React from 'react';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import { Avatar, Card, CardContent, CardHeader, Stack, Link, Container, Grid } from '@mui/material';
import { red } from '@mui/material/colors'
import ProfileEditModal from './profileEditModal';


export default function ProfileSection(props) {
  const [isModalOpen, setOpen] = React.useState(false);
  const handleModalOpen = () => setOpen(true);
  const handleModalClose = () => setOpen(false);

  return (
    <Paper component="main" sx={{ display: 'flex', minHeight: "100vh", flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >

      <CardHeader avatar={
        <Avatar sx={{ bgcolor: red[500], margin: "auto" }} aria-label="user"
        >
          A
        </Avatar>
      }
        title="Abigail Kindle"
        subheader="@abkin">
      </CardHeader>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>15</Link> following</Grid>
          <Grid item><Link href='#' underline='none'>30</Link> followers</Grid>
        </Grid>
      </CardContent>


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
      <ProfileEditModal isOpen={isModalOpen} onClose={handleModalClose} />
    </Paper>
  );
}