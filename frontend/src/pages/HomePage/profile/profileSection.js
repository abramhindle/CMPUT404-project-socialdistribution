import * as React from 'react';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import { Avatar, Container, Typography, Box, Grid, Link, CardHeader, CardContent, IconButton } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import EditIcon from '@mui/icons-material/Edit'
import ProfileEditModal from './profileEditModal';



export default function ProfileSection() {
  const [isModalOpen, setOpen] = React.useState(false);
  const handleModalOpen = () => setOpen(true);
  const handleModalClose = () => setOpen(false);

  const user_id = useSelector(state => state.profile.id);
  const displayName = useSelector(state => state.profile.displayName);
  const github = useSelector(state => state.profile.github);
  const profileImage = useSelector(state => state.profile.profileImage);
  const userURL = useSelector(state => state.profile.url);
  const followerCount = useSelector(state => state.profile.followerCount);
  const followingCount = useSelector(state => state.profile.followingCount);

  return (
    // <Paper component="main" sx={{display: 'flex', minHeight: "100vh", flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >
    //   <Box sx={{ padding: "45px 0 25px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }}>
    //     <Avatar src={profileImage} sx={{ width: "100px", height: "100px" }} />
    //     <Typography variant='h4' sx={{padding: "15px"}}>{displayName}</Typography>
    //     <Typography variant='subtitle1'>{github}</Typography>
    //   </Box>
    // </Paper>

    <Paper component="main" sx={{ display: 'flex', minHeight: "100vh", flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >

      <CardHeader avatar={
        <Avatar sx={{ margin: "auto" }} aria-label="user" src={profileImage} />
      }
        title={displayName}
        subheader={user_id}
        action={
          <IconButton aria-label="settings" onClick={handleModalOpen}>
            <EditIcon />
          </IconButton>
        }
      >
      </CardHeader>
      <CardContent>
        <Grid container spacing={2}>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>15</Link> following</Grid>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>30</Link> followers</Grid>
        </Grid>
      </CardContent>
      <ProfileEditModal isOpen={isModalOpen} onClose={handleModalClose} />
    </Paper>
  );
}