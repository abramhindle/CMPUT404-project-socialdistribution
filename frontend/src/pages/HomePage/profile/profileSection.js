import * as React from 'react';
import Paper from '@mui/material/Paper';
import { Avatar, Container, Typography, Box } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';



export default function ProfileSection() {

  const user_id = useSelector( state => state.profile.id );
  const displayName = useSelector( state => state.profile.displayName );
  const github = useSelector( state => state.profile.github );
  const profileImage = useSelector( state => state.profile.profileImage );
  const userURL = useSelector( state => state.profile.url );

  return (
    <Paper component="main" sx={{display: 'flex', minHeight: "100vh", flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1, }} >
      <Box sx={{ padding: "45px 0 25px 0", display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: "center" }}>
        <Avatar src={profileImage} sx={{ width: "100px", height: "100px" }} />
        <Typography variant='h4' sx={{padding: "15px"}}>{displayName}</Typography>
        <Typography variant='subtitle1'>{github}</Typography>
      </Box>
    </Paper>
  );
}