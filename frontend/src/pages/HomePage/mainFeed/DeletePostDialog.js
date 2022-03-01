import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { deletePost } from '../../../services/posts';

export default function DeletePostDialog({post, alertSuccess, alertError, open, handleClose, removeFromFeed}) {
  const onDelete = () => {
    deletePost(post.id)
      .then( _ => {
        alertSuccess("Success: Deleted Post!");
        removeFromFeed(post);
        handleClose();
      } )
      .catch( err => { 
        console.log(err); 
        alertError("Error: Could Not Delete Post!");
        handleClose();
      } );
  }
    
  return (
      <Dialog open={open} onClose={handleClose} aria-labelledby="alert-dialog-title" aria-describedby="alert-dialog-description" >
        <DialogTitle id="delete-post-title">Delete Post</DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-post-content">Are you sure you want to delete this post?</DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={onDelete}>Delete</Button>
        </DialogActions>
      </Dialog>
  );
}