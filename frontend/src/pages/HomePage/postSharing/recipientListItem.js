import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar } from '@mui/material';
import { useState } from 'react';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import IconButton from '@mui/material/IconButton';
import SendIcon from '@mui/icons-material/Send';
import {createPost} from "../../../Services/posts"
import { useSelector, useDispatch } from 'react-redux';


export default function RecipientListItem({followers, post, alertSuccess, alertError}) {
    const [dense, setDense] = React.useState(false);
    const author = useSelector(state => state.profile);
    // handler for sending share request
    const handleSending = () => {
      post.source = author.url
      post.title = author.displayName + " Share you this post: " + post.title 
      // console.log("post is: ", post.title)
      //source dont match origin mean post is not yours
      createPost(post, followers.id)
        .then( res => { 
          alertSuccess("Success: Sharing post to " + followers.displayName + "!");
        })
        .catch( err => {console.log(err)
          alertError("Error: Could Not Sharing post to " + followers.displayName + "!");
        } );
        
    };
    return (
        <List dense={dense}>
            <ListItem
              secondaryAction={
                <IconButton edge="end" aria-label="send" onClick={handleSending}>
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