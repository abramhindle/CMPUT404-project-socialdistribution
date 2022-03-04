import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { deleteComments } from '../../../services/comments';

export default function DeletePostDialog({commentData, alertSuccess, alertError, open, handleClose}) {

  const onDelete = () => {
    // deleteComments(post.id)
    //   .then( _ => {
    //     alertSuccess("Success: Deleted Comment!");
    //     // removeFromFeed(post);
    //     handleClose();
    //   } )
    //   .catch( err => { 
    //     console.log(err); 
    //     alertError("Error: Could Not Delete Comment!");
    //     handleClose();
    //   } );
  }
    
  return (
      <Dialog open={open} onClose={handleClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description" >
        <DialogTitle id="delete-comment-title">Delete Comment</DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-comment-content">Are you sure you want to delete this comment?</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={onDelete}>Delete</Button>
        </DialogActions>
      </Dialog>
  );
}