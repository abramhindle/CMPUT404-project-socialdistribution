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
import Grid from '@mui/material/Grid';
import CommentCard from '../comment/CommentCard';
import { getComments } from '../../../Services/comments';
import EditPostDialog from './EditPostDialog';
import DeletePostDialog from './DeletePostDialog';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import EditIMGDialog from "./EditIMGDialog"
import AddCommentsDialog from "../comment/addCommentDialog"
import Button from '@mui/material/Button';
import { ReactMarkdown } from 'react-markdown/lib/react-markdown';
import { concat } from 'lodash/fp';

const AvatarContainer = styled('div')({display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", width: "125px"});

const PostImage = styled('img')({width: "100%"})

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
            <ExpandMore expand={expanded} onClick={handleExpandClick} aria-expanded={expanded} aria-label="show more" >
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
  const openDeleteDialog = () => {
    setDeleteOpen(true);
    setAnchorEl(false);
  };

  /* State Hook For Comments */
  const [comments, setComments] = React.useState([]);
  const addComment = comment => setComments(concat(comments)(comment));
  const removeComment = comment => setComments(comments.filter(x => x.id !== comment.id));
  const editComment = comment => setComments(comments.map(x => x.id === comment.id ? comment : x))

  /* State Hook For Menu (edit/remove) */
  const [anchorEl, setAnchorEl] = React.useState(false);

  /* State Hook For Adding comment*/
  const [addCMOpen, setaddCMOpen] = React.useState(false);

  /* Hook handler For Menu (edit/remove) */
  const handleClick = event => setAnchorEl(event.currentTarget);
  const handleClose = () => setAnchorEl(null);
  
  const handleColor = (event) =>setColor("secondary");

  const handleAddCMClickOpen = () => setaddCMOpen(true);

  const handleAddCMClose = () => setaddCMOpen(false);

  /* This Runs When The Button To Show Comments Is Clicked */
  const handleExpandClick = () => {
    getComments(post.id)
      .then( res => { 
        setComments(res.data.items);
        setExpanded(!expanded);
      })
      .catch( err => console.log(err) );
  };

  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={ 
          <AvatarContainer onClick={() => console.log(post.author.id)} >
            <Avatar src={post.author.profileImage} sx={{ width: 64, height: 64,  }} aria-label="recipe" />
            <Typography variant="caption" display="block" gutterBottom sx={{paddingTop: "5px"}}>{post.author.displayName}</Typography>
          </AvatarContainer>
        }
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
        {(post.contentType === "text/plain")&&<Box sx={{width: "100%", px: "20px"}}>
          {post.content.split("\n").map((p, index) => <Typography key={index} paragraph> {p} </Typography>)}
        </Box>}
        {(post.contentType === "text/markdown")&&<Box sx={{width: "100%", px: "20px"}}>
          <ReactMarkdown components={{img: PostImage}}>{post.content}</ReactMarkdown>
        </Box>}
        {post.contentType.includes("image")&&<Box sx={{width: "100%", px: "20px"}}>
          <img src={post.content} width="100%" alt={post.title}/>
        </Box>}
      </CardContent>
      <CardButtons isOwner={isOwner} handleColor={handleColor} expanded={expanded} handleExpandClick={handleExpandClick} color={color} />
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {comments.map((comment) => ( <Grid item xs={12}> <CommentCard removeComment={removeComment} editComments={editComment} comment={comment} alertSuccess={alertSuccess} alertError={alertError} fullWidth /> </Grid>))}
          <Grid item xs={12} sx={{marginTop: "8px"}}>
            <Card fullwidth sx={{maxHeight: 200, mt:"1%"}}>
            <Button disableElevation={false} sx={{minHeight: "100px", fontSize: "1.15rem"}}  onClick={handleAddCMClickOpen} fullWidth>Add Comment</Button>
            </Card>
          </Grid>
        </CardContent>
      </Collapse>
        <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={anchorEl}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
        >
          {((post.contentType === "text/markdown") || (post.contentType === "text/plain"))&&<MenuItem onClick={openEditDialog}>Edit</MenuItem>}
          {post.contentType.includes("image")&&<MenuItem onClick={openEditIMGDialog}>Edit</MenuItem>}
          <MenuItem onClick={openDeleteDialog}>Remove Post</MenuItem>
        </Menu>
      <DeletePostDialog post={post} alertSuccess={alertSuccess} alertError={alertError} open={deleteOpen} handleClose={closeDeleteDialog} removeFromFeed={removeFromFeed} />
      <EditPostDialog post={post} open={editOpen} onClose={closeEditDialog} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} />
      <EditIMGDialog post={post} open={editIMGOpen} onClose={closeEditIMGDialog} alertError={alertError} alertSuccess={alertSuccess} updateFeed={updateFeed} />
      <AddCommentsDialog open={addCMOpen} handleAddCMClose={handleAddCMClose} post={post} addComment={addComment} alertSuccess={alertSuccess} alertError={alertError}></AddCommentsDialog>
    </Card>
  );
}