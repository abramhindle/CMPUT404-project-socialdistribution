import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import Paper from '@mui/material/Paper';
import {createComment} from "../../../Services/comments"
import { getAuthorFromStorage } from '../../../LocalStorage/profile';


export default function AddCommentsDialog({open, handleAddCMClose, addComment, post, alertSuccess, alertError}) {

  /* This Function Posts Form Data To The Backend For Creating New Comments */
  const handleSubmit = (event) => {
    /* Grab Form Data */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data = {
      type: "comment", 
      comment: String(formData.get("comment")), 
      contentType: String(formData.get("contentType")), 
      author: getAuthorFromStorage(),
    }

    /* Validate Fields */
    const fieldValidator = new RegExp("^\\S+")
    const valid = fieldValidator.test(data.comment) && fieldValidator.test(data.contentType) 

    /* Send Data To backend */
    if (valid) {
      console.log(data);
      createComment(post, data)
        .then( res => { 
          addComment(res.data);
          alertSuccess("Success: Created New Comment!");
        })
        .catch( err => { 
          console.log(err);
          alertError("Error: Could Not Create Comment!");
        })
        .finally(() => handleAddCMClose())
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
      <DialogTitle>Post A Comment</DialogTitle>
      <DialogContent>
          <Paper sx={{width: "100%", mt:2}}>
            <Box sx={{width: "100%", p:"8px"}}>
              <TextField id="comment" name="comment" label="Add Comment Here" placeholder="Add Comment Here" multiline fullWidth />
            </Box>
          </Paper>
            <Stack spacing={2} direction="row">
              <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", p:"8px"}}>
                     <FormControl required fullWidth>
                        <InputLabel id="contentType">Content Type</InputLabel>
                        <Select labelId="contentType" id="contentType" name="contentType" label="contentType" defaultValue={"text/plain"} >
                        <MenuItem value={"text/plain"}>Text</MenuItem>
                        <MenuItem value={"text/markdown"}>Markdown</MenuItem>
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