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

export default function SharingDialog({open, onClose, post}) {

    const followers = useSelector(state => state.followers.items);
    
    // state hook for showing listitem or not 
    const [showingItem, setShowingItem] = React.useState(false)

    const handleVisable = () => {
        setShowingItem(followers.length !== 0 ? true : false);
    }

    React.useEffect( () => {
        handleVisable()
    }, [] );

  return (
    <div>
      <Dialog open={open} onClose={onClose} fullWidth>
        <DialogTitle>Sharing the post</DialogTitle>
        <DialogContent>
          
          {showingItem?
          <Box>
                <DialogContentText>
                    Please choose your recipient below
                </DialogContentText>
              {followers.slice(0, followers.length).map((followers, index) => (
                <Paper sx={{mt:2}}>
                <RecipientListItem followers={followers}></RecipientListItem>
                </Paper>
                ))}
          </Box>
          : <DialogContentText>
                Oops, Looks like you don't have recipient to share with
            </DialogContentText>
        }  
        </DialogContent>
        <UrlSharingBox post={post}></UrlSharingBox>


        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

