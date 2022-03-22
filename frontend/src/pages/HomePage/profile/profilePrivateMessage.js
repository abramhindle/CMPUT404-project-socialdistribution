import * as React from 'react';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import CRPostDialog from "../createPost/CRPostDialog";
import IMGPostDialog from '../createPost/IMGPostDialog';
import ButtonGroup from '@mui/material/ButtonGroup';

export default function ProfilePrivateMessage({alertSuccess, alertError, open, onClose, addToFeed}) {

  const [appear, setAppear] = React.useState(false);
  const handleClose = () => {
      setAppear(false);
  };
  const handleClickOpen = () => {
    setAppear(true);
  };
  const [imgOpen, imgSetOpen] = React.useState(false);
  const imgClose = () => {
    imgSetOpen(false);
  };
  const imgClickOpen = () => {
    imgSetOpen(true);
  };
  const buttons = [
    <Button sx={{minHeight: "45px", fontSize: "1.15rem"}} key="CRPost"  onClick={handleClickOpen} fullWidth>New Post</Button>,
    <Button sx={{minHeight: "45px", fontSize: "1.15rem"}} key="IMGPost" onClick={imgClickOpen} fullWidth>New Image</Button>,
  ];
return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md" sx={{borderRadius: "15px"}}>
        <DialogContent>
            <Grid container>
              <ButtonGroup size="large" variant='text' fullWidth>
                  {buttons}
              </ButtonGroup>
            </Grid>
            <CRPostDialog open={appear} onClose={handleClose} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />
            <IMGPostDialog open={imgOpen} onClose={imgClose} alertError={alertError} alertSuccess={alertSuccess} addToFeed={addToFeed} />
          </DialogContent>
      </Dialog>
  );
}
