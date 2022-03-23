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
import {editComment} from "../../../services/comments"

export default function EditCommentDialog({open, comment, handleClose, alertSuccess, alertError, editComments, onClose}) {
    
    /* Submit Form To Edit Comment */
    const handleSubmit = (event) => {
        /* Grab Data From Form */
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const data = { comment: formData.get("comment"), contentType: formData.get("contentType"), }
    
        /* Validate Fields */
        const fieldValidator = new RegExp("^\\S+")
        const valid = fieldValidator.test(data.comment) && fieldValidator.test(data.contentType) 

        /* Send Data To backend */
        if (valid) {
          editComment(comment, data)
            .then( res => { 
              alertSuccess("Success: Edited Comment!");
              editComments(res.data);
            })
            .catch( err => { 
              console.log(err);
              alertError("Error: Could Not Edit Comment!");
            })
            .finally( onClose );
        } else {
          alertError("Error: Must Fill In All Required Fields!");
        }
    
      }

  return (
    <div>
      
      <Dialog open={open} onClose={handleClose} fullWidth>
      <Box component="form" noValidate autoComplete="off" sx={{p:"2%"}} onSubmit={handleSubmit} >
        <DialogTitle>Edit Comment</DialogTitle>
        <DialogContent>
            <Paper sx={{width: "100%", mt:2}}>
            <Box sx={{width: "100%", p:"8px"}}>
            <TextField margin="dense" id="comment" label="Comment" name="comment" defaultValue={comment.comment} fullWidth multiline />
            </Box>
            </Paper>
            <Stack spacing={2} direction="row">
              <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:"8px"}}>
                  <FormControl required fullWidth>
                    <InputLabel id="contentType">Content Type</InputLabel>
                    <Select labelId="contentType" id="contentType" name="contentType" label="Content Type" defaultValue={comment.contentType} >
                      <MenuItem value={"text/plain"}>Text</MenuItem>
                      <MenuItem value={"text/markdown"}>Markdown</MenuItem>
                    </Select>
                  </FormControl>
                </Box>
              </Paper>
            </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Cancel</Button>
          <Button  type="submit" variant="contained">Save Change</Button>
        </DialogActions>
        </Box>
      </Dialog>
    </div>
  );
}
