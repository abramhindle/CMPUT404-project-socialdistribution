import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import Paper from '@mui/material/Paper';
import {createComments} from "../../../services/comments"
import { useSelector } from 'react-redux';


export default function AddCommentsDialog({open, handleAddCMClose, author, alertSuccess, alertError}) {
  /* Hook For Comment content type */
  const [contentType, setContentType] = React.useState(false);

  /* Hook For User ID */
  const userID = useSelector( state => state.profile.url );

  const handleContentTypeChange = (event) => {
    setContentType(event.target.value);
  };

  /* This Function Posts Form Data To The Backend For Creating New Comments */
  const handleSubmit = (event) => {
    /* Grab Form Data */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data = {
      type: "comment", 
      comment: formData.get("comment"), 
      contentType: formData.get("contentType"), 
      author: {author}, 
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
      console.log(data);
      createComments(data, userID)
        .then( res => { 
          alertSuccess("Success: Created New Comment!");
       
          
        })
        .catch( err => { 
          console.log(err);
          alertError("Error: Could Not Create Comment!");
        });
    } else {
      alertError("Error: Must Fill In All Required Fields!");
    }
  };


  return (
    <div>
      
    <Dialog open={open} onClose={handleAddCMClose} fullWidth>
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
                    id="outlined-textarea"
                    label="Add Comment Here"
                    placeholder="Add Comment Here"
                    multiline
                    fullWidth
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
        <Button onClick={handleAddCMClose}>Cancel</Button>
        <Button type="submit" variant="contained">Add Comment</Button>
      </DialogActions>
      </Box>
    </Dialog>
  </div>
    
  );
}