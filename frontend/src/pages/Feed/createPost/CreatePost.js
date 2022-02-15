import * as React from 'react';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Button from '@mui/material/Button';
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
    <Button key="CRPost"  onClick={handleClickOpen} fullWidth>New Post</Button>,
    <Button key="IMGPost" onClick={imgClickOpen} fullWidth>New Image</Button>,
  ];
  return (
    <Paper component="main" sx={{display: 'flex', flexDirection: 'column', evaluation: 2, border: '1px solid lightgrey', boxShadow: 1, borderRadius: 1 }}> 
        <Box sx={{padding: "10px"}}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <ButtonGroup size="large" variant='text' fullWidth>
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