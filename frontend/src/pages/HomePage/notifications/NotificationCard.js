import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import { styled } from '@mui/material/styles';
import EditIcon from '@mui/icons-material/Edit';
import { ReactMarkdown } from 'react-markdown/lib/react-markdown';
import Stack from '@mui/material/Stack';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { Box } from '@mui/system';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import { CardActions, CardHeader } from '@mui/material';
import { deleteNotification } from '../../../Services/notifications';

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
  /* Hook For Follow Request Dialog */
  const [acceptOpen, setAcceptOpen] = React.useState(false);
  const handleEditClickOpen = () => setAcceptOpen(true);
  const handleEditClose = () => setAcceptOpen(false);

  /* Hook For comment delete dialog */
  const [deleteOpen, setDeleteOpen] = React.useState(false);
  const handleDelClickOpen = () => setDeleteOpen(true);
  const handleDelClose = () => setDeleteOpen(false);

  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(false);
  const closeAnchorEl = () => setAnchorEl(false);
  const openAnchorEl = () => setAnchorEl(true);

  /* Hook handler For Menu (edit/remove) */
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  /* Callback For Deleting Notifications */
  const onDeleteNotification = () => {
    closeAnchorEl();
    deleteNotification(notification.author.id, notification.id)
      .then( _ => {
        removeNotification(notification);
        alertSuccess("Successfully Deleted Notification!");
      } )
      .catch( err => { 
        console.log(err);
        alertError("Error: Could Not Delete Notification!");
      } );
  }

  return (
    <Card fullwidth sx={{maxHeight: 200, my: "1px"}}>
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
          <CardButton onClick={() => console.log("Accept")}>Accept</CardButton>
          <CardButton type="submit">Reject</CardButton>
      </CardActions> }
    </Card>
  );
}