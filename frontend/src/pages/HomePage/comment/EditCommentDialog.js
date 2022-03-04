import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import {editComments} from "../../../Services/comments"

export default function EditCommentDialog({open, commentData, handleClose, author, alertSuccess, alertError}) {
    /* Hook For Comment content type */
  const [contentType, setContentType] = React.useState(false);

  const handleContentTypeChange = (event) => {
    setContentType(event.target.value);
  };
    const handleSubmit = (event) => {
        /* Grab Data From Form */
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const data = {
            type: "comment", 
            comment: formData.get("comment"), 
            contentType: formData.get("contentType"), 
            author: author, 
            published: formData.get("published"), 
            id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments/f6255bb01c648fe967714d52a89e8e9c"
          }
          console.log("unlisted data here!!!!", data)
    
        /* Validate Fields */
        // const listValidator = new RegExp("^\\w+[,]?")
        const fieldValidator = new RegExp("^\\w+")
        const valid = fieldValidator.test(data.comment) && fieldValidator.test(data.contentType) 

        /* Send Data To backend */
        if (valid) {
        //   editComments(data, cmID)
        //     .then( res => { 
        //       alertSuccess("Success: Edited Comment!");
        //       updateFeed(res.data);
        //       onClose();
        //     })
        //     .catch( err => { 
        //       console.log(err);
        //       alertError("Error: Could Not Edit Comment!");
        //     });
        } else {
          alertError("Error: Must Fill In All Required Fields!");
        }
    
      }

  return (
    <div>
      
      <Dialog open={open} onClose={handleClose} fullWidth>
      <Box
        component="form"
        noValidate
        autoComplete="off"
        sx={{p:"2%"}}
        onSubmit={handleSubmit}
        >
        <DialogTitle>Edit Comment</DialogTitle>
        <DialogContent>
            <Paper sx={{width: "100%", mt:2}}>
            <Box sx={{width: "100%", p:"8px"}}>
            <TextField
                autoFocus
                margin="dense"
                id="comments"
                label="Comments"
                name="comment"
                defaultValue={commentData.comment}
                fullWidth
                multiline
            />
            </Box>
            </Paper>
            <Stack spacing={2} direction="row">
              <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", p:"8px"}}>
                     <FormControl required fullWidth>
                        <InputLabel id="contentType">Content Type</InputLabel>
                        <Select
                          labelId="contentType"
                          id="contentType"
                          name="contentType"
                          label="contentType"
                          defaultValue={commentData.contentType}
                          onChange={handleContentTypeChange}
                        >
                        <MenuItem value={"text"}>Text</MenuItem>
                        <MenuItem value={"markdown"}>Markdown</MenuItem>
                        </Select>
                    </FormControl>
                    </Box>
                  </Paper>

            </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button  type="submit" variant="contained">Save Change</Button>
        </DialogActions>
        </Box>
      </Dialog>
    </div>
  );
}
