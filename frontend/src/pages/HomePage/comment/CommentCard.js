import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import EditCommentDialog from './EditCommentDialog';
import EditIcon from '@mui/icons-material/Edit';

/* 
 * Takes the date formatted according to the ISO standard and returns the date formatted in the form "March 9, 2016 - 6:07 AM"
 */
function isoToHumanReadableDate(isoDate) {
  const date = new Date(isoDate);
  const dateFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'long', day: 'numeric' });
  const timeFormat = new Intl.DateTimeFormat('en', { hour: 'numeric', minute: 'numeric' });
  return dateFormat.format(date) + " - " + timeFormat.format(date);
}

export default function CommentCard(props) {
  /* Hook For Like icon color */
  const [color, setColor] = React.useState("grey");
  /* Hook For comment edit dialog */
  const [open, setOpen] = React.useState(false);

  const handleColor = (event) =>{
    setColor("secondary")
  }

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  

  return (
    <Card fullwidth sx={{maxHeight: 200, mt:"1%"}}>
      <Grid container direction={'row'} spacing={5}>
        <Grid item xl={11} md={11} sm={10} xs={10}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            {props.commentData.comment}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {isoToHumanReadableDate(props.commentData.published)}
          </Typography>
        </CardContent>
        </Grid>
        <Grid item xl={1} md={1} sm={2} xs={2}>
          <IconButton aria-label="like">
            <FavoriteIcon color = {color} onClick={handleColor}/>
          </IconButton>
          <IconButton aria-label="Edit comment">
            <EditIcon onClick={handleClickOpen}/>
          </IconButton>
        </Grid>
      </Grid>
      <EditCommentDialog open={open} handleClose={handleClose} commentData={props.commentData} alertSuccess={props.alertSuccess} alertError={props.alertError}></EditCommentDialog>
    </Card>
  );
}