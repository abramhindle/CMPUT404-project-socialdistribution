import * as React from 'react';
import { useState } from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';
import ProfilePrivateMessage from './profilePrivateMessage';
import { set, concat } from 'lodash/fp';
import Box from '@mui/material/Box';
import { setInboxInStorage, getInboxFromStorage } from '../../../LocalStorage/inbox';
import { getAuthorFromStorage, setAuthorInStorage  } from '../../../LocalStorage/profile';
import DeleteFollowingDialog from './deleteFollowingDialog';
import { useSelector } from 'react-redux';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
export default function ProfileListItem({type, author, profile, removeProfile, alertError, alertSuccess, addToFeed}) {
    const [open, setOpen] = React.useState(false);
    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };
    const [appear, setAppear] = React.useState(false);
    const appearClose = () => {
        setAppear(false);
    };
    const handleClickAppear = () => {
      setAppear(true);
    };

    return (
        <Box>
        <ListItemButton sx={{ pl: 4 }} >
            <ListItemAvatar>
                <Avatar alt={profile.displayName} src={profile.profileImage} />
            </ListItemAvatar>
            <ListItemText primary={profile.displayName} />
            <Button sx={{minHeight: "45px", fontSize: "1.15rem"}} key="CRPost"  onClick={handleClickAppear} fullWidth>Send Post</Button>
            {type === "following" && <Button sx={{minHeight: "45px", fontSize: "1.15rem"}} key="IMGPost" onClick={handleClickOpen} fullWidth>Unfollow</Button>}
        </ListItemButton>
        <ProfilePrivateMessage open={appear} onClose={appearClose} profile={profile} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />
        {type === "following" && <DeleteFollowingDialog author={author} following={profile} alertSuccess={alertSuccess} alertError={alertError} open={open} handleClose={handleClose} removeFollowing={removeProfile}/>}
        </Box>
        );
    }

        
// import DeleteFollowingDialog from './deleteFollowingDialog';
// import { useSelector } from 'react-redux';
// import { useState } from 'react';

// export default function ProfileListItem({type, author, profile, removeProfile, alertError, alertSuccess}) {

//     const [open, setOpen] = useState(false);
//     const handleClose = () => setOpen(false);

//     return (
//         <div>
//             <ListItemButton sx={{ pl: 3 }} onClick={() => setOpen(true)}>
//                 <ListItemAvatar>
//                     <Avatar alt={profile.displayName} src={profile.profileImage} />
//                 </ListItemAvatar>
//                 <ListItemText primary={profile.displayName} />
//             </ListItemButton>
//             {type === "following" && <DeleteFollowingDialog author={author} following={profile} alertSuccess={alertSuccess} alertError={alertError} open={open} handleClose={handleClose} removeFollowing={removeProfile} />}
//         </div>
//     );
// }