import * as React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import ButtonGroup from '@mui/material/ButtonGroup';
import CRPostDialog from "./CRPostDialog";
import IMGPostDialog from './IMGPostDialog';



export default function CreatePost({alertSuccess, alertError, addToFeed}) {

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
    <Button sx={{minHeight: "45px", fontSize: "1.15rem"}} key="CRPost"  onClick={handleClickOpen} fullWidth>New Post</Button>,
    <Button sx={{minHeight: "45px", fontSize: "1.15rem"}} key="IMGPost" onClick={imgClickOpen} fullWidth>New Image</Button>,
  ];
  return (
    <Paper component="main" sx={
      { display: 'flex'
      , minHeight: "45px"
      , flexDirection: 'column'
      , evaluation: 2, border: '1px solid lightgrey'
      , boxShadow: 1
      , justifyContent: "center"
      , borderRadius: 1 }
    }> 
        <Box sx={{padding: "10px"}}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <ButtonGroup size="large" variant='text' fullWidth>
                  {buttons}
              </ButtonGroup>
            </Grid>
          </Grid>
        </Box>
        <CRPostDialog open={open} onClose={handleClose} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />
        <IMGPostDialog open={imgOpen} onClose={imgClose}></IMGPostDialog>
      </Paper>
  );
}