import * as React from 'react';
import { styled } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Collapse from '@mui/material/Collapse';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import { red } from '@mui/material/colors';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ShareIcon from '@mui/icons-material/Share';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Box from '@mui/material/Box';
import CommentIcon from '@mui/icons-material/Comment';
import Menu from '@mui/material/Menu';
import Grid from '@mui/material/Grid';
import MenuItem from '@mui/material/MenuItem';
import CommentCard from '../comment/CommentCard';

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

export default function FeedCard(props) {
  const [image, setImage] = React.useState("")
  const [content, setContent] = React.useState("")
  const [expanded, setExpanded] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [color, setColor] = React.useState("grey");
  const [show, setShow] = React.useState(false);
  const [textShow, setTextShow] = React.useState(false);
  const open = Boolean(anchorEl);
  
  
  const handleColor = (event) =>{
    setColor("secondary")
  }
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };
  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  React.useEffect(()=>{
      if (props.feedData !== undefined){
          setImage(props.feedData ? props.feedData.ImgUrl : undefined)
          setContent(props.feedData ? props.feedData.content : undefined)
      }
      if(image !== undefined && image !== ""){
        setShow(true)
      }
      if (content !== undefined && content !== ""){
        setTextShow(true)
      }
      
  }, [props.feedData, image, content])

  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={ <Avatar src={props.feedData.author.profileImage} sx={{ width: 64, height: 64,  }} aria-label="recipe" />}
          action={
          <IconButton aria-label="settings" onClick={handleClick}>
            <MoreVertIcon id="setting-button" aria-controls={open ? 'setting-menu' : undefined} aria-haspopup="true" aria-expanded={open ? 'true' : undefined} />
          </IconButton> }
        title={<Typography variant='h6'>{props.feedData.title}</Typography> }
        subheader={
          <span>
            <Typography variant='subheader'>{props.feedData.description}</Typography><br/>
            <Typography variant='subheader'>{isoToHumanReadableDate( props.feedData.published )}</Typography>
          </span> }
        disableTypography={true}
      />
      <Menu
        id="setting-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{ 'aria-labelledby': 'setting-button', }} 
      >
        <MenuItem onClick={handleClose}>Edit</MenuItem>
      </Menu>
      <CardContent>
        {textShow && 
            <Box sx={{width: "100%", px: "80px", }}>
              <Typography paragraph>
                {props.feedData.content}
              </Typography>
          </Box> }
      </CardContent>
      {show && <Box>
        <CardMedia
        component="img"
        image={"https://cdn.pixabay.com/photo/2019/05/08/21/21/cat-4189697_1280.jpg"}
        alt="Feed Image"
        />
        </Box>}
      
      <CardActions disableSpacing>
        <IconButton aria-label="like" onClick={handleColor}>
          <FavoriteIcon color = {color}/>
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <CommentIcon />
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          {props.feedData.commentsSrc.comments.map((commentData) => (
                        <Grid item xs={12}>
                            <CommentCard commentData={commentData} fullWidth={true} />
                        </Grid>
                        ))}
        </CardContent>
      </Collapse>
    </Card>
  );
}