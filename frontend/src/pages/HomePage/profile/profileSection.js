import * as React from 'react';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';
import { Avatar, Container, Typography, Box, Grid, Link, CardHeader, CardContent, IconButton, ListItemButton, Collapse, ListItemAvatar } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import EditIcon from '@mui/icons-material/Edit'
import ProfileEditModal from './profileEditModal';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import ProfileListItem from './profileListItem';



export default function ProfileSection({author, editAuthor}) {
  const [isModalOpen, setOpen] = React.useState(false);
  const [isFollowingOpen, setFollowingOpen] = React.useState(true);
  const [isFollowerOpen, setFollowerOpen] = React.useState(true);
  const handleFollowing = () => {
    setFollowingOpen(!isFollowingOpen);
  };
  const handleFollower = () => {
    setFollowerOpen(!isFollowerOpen);
  };

  const handleModalOpen = () => setOpen(true);
  const handleModalClose = () => setOpen(false);

  const user_id = author.id;
  const displayName = author.displayName;
  const github = author.github;
  const profileImage = author.profileImage;
  const userURL = author.url;
  const followerCount = author.followerCount;
  const followingCount = author.followingCount;

  const style = {
    list: {
      maxHeight: '32rem',
      overflow: 'auto',
      // marginBottom: '2rem',
    },
    listHeader: {
      background: '#f5f5f5'
    }
  };

  return (
    // <Paper component="main" sx={{display: 'flex', minHeight: "100vh", flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >
    //   <Box sx={{ padding: "45px 0 25px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }}>
    //     <Avatar src={profileImage} sx={{ width: "100px", height: "100px" }} />
    //     <Typography variant='h4' sx={{padding: "15px"}}>{displayName}</Typography>
    //     <Typography variant='subtitle1'>{github}</Typography>
    //   </Box>
    // </Paper>

    <Paper component="main" sx={{ display: 'flex', flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >

       <Box sx={{ padding: "45px 0 25px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }}>
         <Avatar src={profileImage} sx={{ width: "100px", height: "100px" }} />
         <Typography variant='h4' sx={{padding: "15px"}}>{displayName}</Typography>
         <Typography variant='subtitle1'>{github}</Typography>
       </Box>
      {<CardContent>
        <Grid container spacing={2}>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>15</Link> following</Grid>
          <Grid item><Link onClick={handleModalOpen} href='#' underline='none'>30</Link> followers</Grid>
        </Grid>
      </CardContent>}

      <Divider />
            {Array(10).fill(null).map((n, index) => (
              <ProfileListItem key={index} displayName={'User ' + index} profileImage={profileImage} />
            ))}


            {Array(10).fill(null).map((n, index) => (
              <ProfileListItem key={index} displayName={'User ' + index} profileImage={profileImage} />
            ))}

      <ProfileEditModal isOpen={isModalOpen} onClose={handleModalClose} />
    </Paper>
  );
}
