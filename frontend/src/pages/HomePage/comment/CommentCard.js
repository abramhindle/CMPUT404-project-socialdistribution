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
import DeleteCommentDialog from "../comment/DeleteCommentDialog"
import Stack from '@mui/material/Stack';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

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
  const [editOpen, setEditOpen] = React.useState(false);
  /* Hook For comment delete dialog */
  const [deleteOpen, setDeleteOpen] = React.useState(false);
  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(false);

  const handleColor = () =>{
    setColor("secondary")
    
  }


  const handleEditClickOpen = () => {
    setEditOpen(true);
  };

  const handleEditClose = () => {
    setEditOpen(false);
  };

  const handleDelClickOpen = () => {
    setDeleteOpen(true);
  };

  const handleDelClose = () => {
    setDeleteOpen(false);
  };

  /* Hook handler For Menu (edit/remove) */
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };


    

  

  return (
    <Card fullwidth sx={{maxHeight: 200, mt:"1%"}}>
      <Grid container direction={'row'} spacing={12}>
        <Grid item xl={10} md={10}>
        <CardContent>
          <Stack direction="row" spacing={2}>
            <Typography gutterBottom variant="h6" component="div">
              {props.commentData.author.type}
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{pt: 1}}>
              {isoToHumanReadableDate(props.commentData.published)}
            </Typography>
          </Stack>
          <Typography variant="body2" color="text.primary" >
              {props.commentData.comment}
            </Typography>
        </CardContent>
        </Grid>
        <Grid item xl={1} md={1}>
        <Stack direction="row" spacing={1} sx={{pt:1}}>
          <IconButton aria-label="like" onClick={handleColor}>
            <FavoriteIcon color = {color}/>
          </IconButton>
          <IconButton aria-label="settings" onClick={handleClick}>
            <MoreVertIcon />
          </IconButton>
          </Stack>
        </Grid>
      </Grid>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={anchorEl}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
        >
          <MenuItem onClick={handleEditClickOpen}>Edit</MenuItem>
          <MenuItem onClick={handleDelClickOpen}>Remove</MenuItem>
        </Menu>
      <EditCommentDialog open={editOpen} handleClose={handleEditClose} commentData={props.commentData} alertSuccess={props.alertSuccess} alertError={props.alertError}></EditCommentDialog>
      <DeleteCommentDialog open={deleteOpen} handleClose={handleDelClose} commentData={props.commentData} alertSuccess={props.alertSuccess} alertError={props.alertError}></DeleteCommentDialog>
    </Card>
  );
}