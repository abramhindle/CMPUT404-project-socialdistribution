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
// import ProfileListItem from '../profile/profileListItem';

export default function SharingDialog({open, onClose}) {

    const followers = useSelector(state => state.followers.items);
    // console.log("followers is:", followers)
    
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
          <DialogContentText>
            Please choose your recipient below
          </DialogContentText>
          {showingItem?
          <Box sx={{pt:2}}>
              {followers.slice(0, followers.length).map((followers, index) => (
                <Paper>
                <RecipientListItem followers={followers}></RecipientListItem>
                </Paper>
                ))}
          </Box>
          : <></>}  
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

