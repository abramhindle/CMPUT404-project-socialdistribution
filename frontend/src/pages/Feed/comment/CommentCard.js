import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import FavoriteIcon from '@mui/icons-material/Favorite';
import IconButton from '@mui/material/IconButton';

export default function CommentCard(props) {
  const [color, setColor] = React.useState("grey");
  const handleColor = (event) =>{
    setColor("secondary")
  }
  return (
    <Card fullwidth sx={{maxHeight: 200}}>
      <Grid container direction={'row'} spacing={5}>
        <Grid item xl={11} md={11} sm={10} xs={10}>
        <CardContent>
          <Typography gutterBottom variant="h5" component="div">
            Lizard
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Lizards are a widespread group of squamate reptiles, with over 6,000
            species, ranging across all continents except Antarctica
          </Typography>
        </CardContent>
        </Grid>
        <Grid item xl={1} md={1} sm={2} xs={2}>
          <IconButton aria-label="like">
            <FavoriteIcon color = {color} onClick={handleColor}/>
          </IconButton>
        </Grid>
</Grid>
      
      
    </Card>
  );
}