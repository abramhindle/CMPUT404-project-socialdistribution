import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';
import DeleteFollowingDialog from './deleteFollowingDialog';
import { useSelector } from 'react-redux';
import { useState } from 'react';

export default function ProfileListItem({type, author, profile, removeProfile, alertError, alertSuccess}) {

    const [open, setOpen] = useState(false);
    const handleClose = () => setOpen(false);

    return (
        <div>
            <ListItemButton sx={{ pl: 3 }} onClick={() => setOpen(true)}>
                <ListItemAvatar>
                    <Avatar alt={profile.displayName} src={profile.profileImage} />
                </ListItemAvatar>
                <ListItemText primary={profile.displayName} />
            </ListItemButton>
            {type === "following" && <DeleteFollowingDialog author={author} following={profile} alertSuccess={alertSuccess} alertError={alertError} open={open} handleClose={handleClose} removeFollowing={removeProfile} />}
        </div>
    );
}