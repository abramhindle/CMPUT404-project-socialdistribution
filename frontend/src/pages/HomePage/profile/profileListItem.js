import * as React from 'react';
import { useState } from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';
import ProfilePrivateMessage from './profilePrivateMessage';
import { set, concat } from 'lodash/fp';
import Box from '@mui/material/Box';
import { setInboxInStorage, getInboxFromStorage } from '../../../LocalStorage/inbox';
import { getAuthorFromStorage, setAuthorInStorage  } from '../../../LocalStorage/profile';
export default function ProfileListItem(props) {
    const [open, setOpen] = React.useState(false);
    const handleClickOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };
    /* Add A New Item To The Notification */
    const addToFeed = (item) => {
        const newInbox = concat(inbox)(item).sort((a, b) => Date.parse(b.published) - Date.parse(a.published));
        setInbox(newInbox);
        setInboxInStorage(newInbox);
    }

    /* State Hook For Inbox */
    const [inbox, setInbox] = useState(getInboxFromStorage()); 

    /* State Hook For Displaying Alerts */
    const [openAlert, setOpenAlert] = useState({isOpen: false, message: "", severity: "error"})
    const alertSuccess = msg => setOpenAlert({isOpen: true, message: msg, severity: "success"})
    const alertError = msg => setOpenAlert({isOpen: true, message: msg, severity: "error"})    
    return (
        <Box>
        <ListItemButton sx={{ pl: 4 }} onClick={handleClickOpen}>
            <ListItemAvatar>
                <Avatar alt={props.displayName} src={props.profileImage} />
            </ListItemAvatar>
            <ListItemText primary={props.displayName} />
        </ListItemButton>
        <ProfilePrivateMessage open={open} onClose={handleClose} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />
        </Box>
        
    );
}