import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { deleteFollowing, deleteFollower } from '../../../services/followers';

export default function DeleteFollowingDialog({author, following, alertSuccess, alertError, open, handleClose, removeFollowing}) {

  const onDelete = () => {
    deleteFollowing(author.url, following.id)
      .then( _ => deleteFollower(following.id, author.url) )
      .then ( _ => removeFollowing(following) )
      .then( _ => alertSuccess("Success: Stopped Following " + following.displayName + "!"))
      .catch( err => { console.log(err); alertError("Error: Could Not Delete Comment!"); } )
      .finally( () => handleClose() );
  }
    
  return (
      <Dialog open={open} onClose={handleClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description" >
        <DialogTitle id="delete-comment-title">Stop Following </DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-comment-content">Are you sure you want to stop following {following.displayName}?</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={onDelete}>Remove</Button>
        </DialogActions>
      </Dialog>
  );
}