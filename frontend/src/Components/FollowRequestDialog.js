
import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { getAuthorFromStorage } from '../LocalStorage/profile';
import { pushToInbox } from '../Services/inbox';
import { addFollowing } from '../Services/followers';

export default function FollowRequestDialog({authorToFollow, alertSuccess, alertError, open, handleClose}) {

  const author = getAuthorFromStorage();

  const onSendFollow = () => {
    const data = {
        "type": "follow",      
        "summary": author.displayName + " wants to follow " + authorToFollow.displayName,
        "actor": author, 
        "object": authorToFollow, 
    };
    console.log(JSON.stringify(data));
    pushToInbox(authorToFollow.id, data)
        .then( _ => addFollowing(author.url, authorToFollow.id) )
        .then( _ => alertSuccess("Follow Request Sent!") )
        .catch( err => { console.log(err); alertError("Error: Could Not Send Follow Request!"); } )
        .finally( handleClose );
  }
    
  return (
      <Dialog open={open} onClose={handleClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description" >
        <DialogTitle id="delete-comment-title">Send Follow Request</DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-comment-content">{"Do You Want To Follow " + authorToFollow.displayName + "?"}</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={onSendFollow}>Send</Button>
        </DialogActions>
      </Dialog>
  );
}