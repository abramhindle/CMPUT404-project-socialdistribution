import * as React from 'react';
import Card from '@mui/material/Card';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import { useSelector, useDispatch } from 'react-redux';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { CardActions, CardHeader } from '@mui/material';
import { deleteNotification } from '../../../services/notifications';
import { addFollower, getFollowers } from '../../../services/followers';
import { setFollowers } from '../../../redux/followersSlice';


const CardButton = styled(Button)({fontSize: "1.2rem", fontWeight: 500});

/* 
 * Takes the date formatted according to the ISO standard and returns the date formatted in the form "March 9, 2016 - 6:07 AM"
 */
function isoToHumanReadableDate(isoDate) {
  const date = new Date(isoDate);
  const dateFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'long', day: 'numeric' });
  const timeFormat = new Intl.DateTimeFormat('en', { hour: 'numeric', minute: 'numeric' });
  return dateFormat.format(date) + " - " + timeFormat.format(date);
}

export default function NotificationCard({notification, alertSuccess, alertError, removeNotification}) {
  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(false);
  const closeAnchorEl = () => setAnchorEl(false);

  /* State Hook For Updating Followers */
  const dispatch = useDispatch();

  /* State Hook For Author */
  const author = useSelector(state => state.profile);

  /* Callback For Deleting Notifications */
  const onDeleteNotification = () => {
    closeAnchorEl();
    deleteNotification(notification.author.id, notification.id)
      .then( _ => removeNotification(notification) )
      .then( _ => alertSuccess("Successfully Deleted Notification!"))
      .catch( err => { console.log(err); alertError("Error: Could Not Delete Notification!"); } );
  }

  /* Callback For Accepting Follow Requests */
  const onAcceptFollow = () => {
    addFollower(notification.author.id, notification.actor)
      .then( _ => Promise.all([deleteNotification(notification.author.id, notification.id), getFollowers(author.id)]))
      .then( values => dispatch(setFollowers(values[1].data.items)) )
      .then( _ => removeNotification(notification) )
      .then( _ => alertSuccess("Accepted Follow Request!") )
      .catch( err => { console.log(err); alertError("Error: Could Not Accept Follow Request!"); } );
  }

  return (
    <Card fullwidth="true" sx={{maxHeight: 200, my: "1px"}}>
        <CardHeader 
          sx={{paddingBottom: notification.type === "Follow" ? "0px" : "16px"}}
          action={ <IconButton aria-label="settings" onClick={event => setAnchorEl(event.currentTarget)}> <MoreVertIcon /> </IconButton> } 
          title={<Typography gutterBottom variant="h4" component="div"> {notification.summary} </Typography>}
          subheader={isoToHumanReadableDate(notification.published)}
        />
      <Menu id="basic-menu" anchorEl={anchorEl} open={anchorEl} onClose={closeAnchorEl} MenuListProps={{ 'aria-labelledby': 'basic-button', }} >
          <MenuItem onClick={onDeleteNotification}>Delete</MenuItem>
      </Menu>
      {notification.type === "Follow"&&
      <CardActions>
          <CardButton onClick={onAcceptFollow}>Accept</CardButton>
          <CardButton type="submit" onClick={onDeleteNotification}>Reject</CardButton>
      </CardActions> }
    </Card>
  );
}