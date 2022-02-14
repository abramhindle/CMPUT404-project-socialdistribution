import * as React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import PostAddIcon from '@mui/icons-material/PostAdd';
import Grid from '@mui/material/Grid';
import ButtonGroup from '@mui/material/ButtonGroup';
import CRPostDialog from "./CRPostDialog";
import IMGPostDialog from './IMGPostDialog';



export default function CreatePost() {
  const [open, setOpen] = React.useState(false);
  const [imgOpen, imgSetOpen] = React.useState(false);
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  const imgClickOpen = () => {
    imgSetOpen(true);
  };

  const imgClose = () => {
    imgSetOpen(false);
  };
  const buttons = [
    <Button key="CRPost" sx={{borderRadius:"18px"}} onClick={handleClickOpen}>Start a Post</Button>,
    <Button key="IMGPost" sx={{borderRadius:"18px"}} onClick={imgClickOpen}>Image Post</Button>,
  ];
  return (
    <Paper component="main" sx={{display: 'flex', flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 5 }}> 
        <Box sx={{padding: "10px"}}>
        <Grid container spacing={2}>
                <Grid item xs={4}>
                    <PostAddIcon fontSize="large"/>
                </Grid>
                <Grid item xs={8}>
                    <ButtonGroup size="large" aria-label="large button group">
                        {buttons}
                    </ButtonGroup>
                </Grid>
            </Grid>
        </Box>
        <CRPostDialog open={open} onClose={handleClose}></CRPostDialog>
        <IMGPostDialog open={imgOpen} onClose={imgClose}></IMGPostDialog>
      </Paper>
  );
}