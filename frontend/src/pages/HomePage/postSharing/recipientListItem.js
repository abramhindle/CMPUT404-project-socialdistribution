


import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';
import { useSelector } from 'react-redux';
import { useState } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import DeleteIcon from '@mui/icons-material/Delete';
import FolderIcon from '@mui/icons-material/Folder';
import IconButton from '@mui/material/IconButton';
import SendIcon from '@mui/icons-material/Send';


export default function RecipientListItem({followers}) {
    const [dense, setDense] = React.useState(false);
    return (
        <List dense={dense}>
            <ListItem
              secondaryAction={
                <IconButton edge="end" aria-label="send">
                  <SendIcon />
                </IconButton>
              }
            >
              <ListItemAvatar>
                <Avatar alt={followers.displayName} src={followers.profileImage} />
              </ListItemAvatar>
              <ListItemText
                primary={followers.displayName}
              />
            </ListItem>
        </List>

    );
}