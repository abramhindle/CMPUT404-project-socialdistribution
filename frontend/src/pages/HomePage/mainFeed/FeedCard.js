import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import Box from '@mui/material/Box';
import CommentIcon from '@mui/icons-material/Comment';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import Grid from '@mui/material/Grid';
import CommentCard from '../comment/CommentCard';
import { getComments } from '../../../services/comments';
import EditPostDialog from './EditPostDialog';
import DeletePostDialog from './DeletePostDialog';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import EditIMGDialog from "./EditIMGDialog"

/* 
 * Takes the date formatted according to the ISO standard and returns the date formatted in the form "March 9, 2016 - 6:07 AM"
 */
function isoToHumanReadableDate(isoDate) {
  const date = new Date(isoDate);
  const dateFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'long', day: 'numeric' });
  const timeFormat = new Intl.DateTimeFormat('en', { hour: 'numeric', minute: 'numeric' });
  return dateFormat.format(date) + " - " + timeFormat.format(date);
}
const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

function CardButtons({isOwner, handleColor, expanded, handleExpandClick, color}) {
  return (
      <CardActions disableSpacing>
        <IconButton aria-label="like" onClick={handleColor}>
          <FavoriteIcon color = {color}/>
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
        <div sx={{pr:8}}>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <CommentIcon/>
        </ExpandMore>
        </div>
      </CardActions>
  )
}


export default function FeedCard({post, isOwner, alertError, alertSuccess, updateFeed, removeFromFeed}) {
  /* State Hook For Expanding The Comments */
  const [expanded, setExpanded] = React.useState(false);

  /* State Hook For Colour Scheme */
  const [color, setColor] = React.useState("grey");

  /* State Hook For Opening Edit Post Dialog */
  const [editOpen, setEditOpen] = React.useState(false);
  const closeEditDialog = () => setEditOpen(false);
  const openEditDialog = () => setEditOpen(true);
  /* State Hook For Opening Edit IMG Post Dialog */
  const [editIMGOpen, setEditIMGOpen] = React.useState(false);
  const closeEditIMGDialog = () => setEditIMGOpen(false);
  const openEditIMGDialog = () => setEditIMGOpen(true);

  /* State Hook For Opening Delete Post Dialog */
  const [deleteOpen, setDeleteOpen] = React.useState(false);
  const closeDeleteDialog = () => setDeleteOpen(false);
  const openDeleteDialog = () => setDeleteOpen(true);

  /* State Hook For Comments */
  const [comments, setComments] = React.useState([]);

  /* State Hook For Showing IMG/Text Post */
  const [imgShow, setImgShow] = React.useState(false);

  /* State Hook For Showing IMG/Text Post */
  const [textShow, setTextShow] = React.useState(false);

  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(null);
  const open = Boolean(anchorEl);

  /* Hook handler For Menu (edit/remove) */
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  
  const handleColor = (event) =>{
    setColor("secondary")
  };

   /* Set visible condition for IMG/Text Post */
  React.useEffect(()=>{
    if (post.content.includes("data:")){
      setImgShow(true)
      setTextShow(false)
    }else{
      setImgShow(false)
      setTextShow(true)
    }
}, [post])


  
  /* This Runs When The Button To Show Comments Is Clicked */
  const handleExpandClick = () => {
    getComments("dummy_author", "dummy_post")
      .then( res => { 
        setComments(res);
        setExpanded(!expanded);
      })
      .catch( err => console.log(err) );
  };


  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={ <Avatar src={post.author.profileImage} sx={{ width: 64, height: 64,  }} aria-label="recipe" />}
        title={<Typography variant='h6'>{post.title}</Typography>}
        action={
          <IconButton aria-label="settings" onClick={handleClick}>
            {isOwner ? 
            <MoreVertIcon />
            : <></>} 
          </IconButton>
        }
        subheader={
          <span>
            <Typography variant='subheader'>{post.description}</Typography><br/>
            <Typography variant='subheader'>{isoToHumanReadableDate( post.published )}</Typography>
          </span> }
        disableTypography={true}
      />
      <CardContent>
        {textShow&&<Box sx={{width: "100%", px: "80px"}}>
          <Typography paragraph>
            {post.content}
          </Typography>
        </Box>}
        {imgShow &&<Box sx={{width: "100%"}}>
          <img src={post.content} width="100%" alt={post.title}/>
        </Box>}
      </CardContent>
      <CardButtons isOwner={isOwner} handleColor={handleColor} expanded={expanded} handleExpandClick={handleExpandClick} color={color} />
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {comments.map((commentData) => ( <Grid item xs={12}> <CommentCard commentData={commentData} fullWidth /> </Grid>))}
        </CardContent>
      </Collapse>
        <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
        >
          {textShow&&<MenuItem onClick={openEditDialog}>Edit</MenuItem>}
          {imgShow &&<MenuItem onClick={openEditIMGDialog}>Edit</MenuItem>}
          <MenuItem onClick={openDeleteDialog}>Remove Post</MenuItem>
        </Menu>
      <DeletePostDialog post={post} alertSuccess={alertSuccess} alertError={alertError} open={deleteOpen} handleClose={closeDeleteDialog} removeFromFeed={removeFromFeed} />
      <EditPostDialog post={post} open={editOpen} onClose={closeEditDialog} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} />
      <EditIMGDialog post={post} open={editIMGOpen} onClose={closeEditIMGDialog} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} />
    </Card>
  );
}