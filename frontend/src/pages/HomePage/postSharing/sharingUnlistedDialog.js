import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import { useSelector, useDispatch } from 'react-redux';
import RecipientListItem from "./recipientListItem";
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import UrlSharingBox from './urlSharingBox';


export default function SharingDialog({open, onClose, post, alertSuccess, alertError}) {
    
    
    

  return (
    <div>
      <Dialog open={open} onClose={onClose} fullWidth>
        <DialogTitle>Sharing the unlisted post</DialogTitle>
        <UrlSharingBox post={post}></UrlSharingBox>
      </Dialog>
    </div>
  );
}

