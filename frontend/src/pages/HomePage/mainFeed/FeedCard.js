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
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import Box from '@mui/material/Box';
import CommentIcon from '@mui/icons-material/Comment';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';

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
  const [expanded, setExpanded] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [color, setColor] = React.useState("grey");
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

  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: red[500] }} aria-label="recipe"> R </Avatar>
        }
        action={
          <IconButton aria-label="settings" onClick={handleClick}>
            <MoreVertIcon id="setting-button" aria-controls={open ? 'setting-menu' : undefined} aria-haspopup="true" aria-expanded={open ? 'true' : undefined} />
          </IconButton>
        }
        title="Feed title"
        subheader="September 14, 2016"
      />
      <Menu
        id="setting-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'setting-button',
        }}
      >
        <MenuItem onClick={handleClose}>Edit</MenuItem>
        {/* <MenuItem onClick={handleClose}>Options</MenuItem> */}
      </Menu>
      <CardContent>
        <Typography variant="body2" color="text.secondary">
          Feed description goes here
        </Typography>
      </CardContent>
      <CardMedia
        component="img"
        image={"https://cdn.pixabay.com/photo/2019/05/08/21/21/cat-4189697_1280.jpg"}
        alt="Feed Image"
      />
      <CardActions disableSpacing>
        <IconButton aria-label="like" onClick={handleColor}>
          <FavoriteIcon color = {color}/>
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
        <IconButton aria-label="comment">
          <CommentIcon />
        </IconButton>
        <ExpandMore
          expand={expanded}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </ExpandMore>
      </CardActions>
      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
          <Typography paragraph>Detail:</Typography>
          <Typography paragraph>
            Feed detail goes here
          </Typography>
        </CardContent>
      </Collapse>
    </Card>
  );
}