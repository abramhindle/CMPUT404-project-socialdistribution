import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { editPost } from '../../../services/posts';

export default function EditPostDialog({post, alertSuccess, alertError, open, onClose, updateFeed}) {

  const onSubmit = (event) => {
    /* Grab Data From Form */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data = {
      type: "post", 
      title: formData.get("title"), 
      description: formData.get("description"), 
      contentType: post.contentType, 
      content: formData.get("content"), 
      categories: formData.get("categories").replaceAll(" ", "").split(","), 
      visibility: post.visibility, 
      unlisted: post.unlisted
    }

    /* Validate Fields */
    const listValidator = new RegExp("^\\w+[,]?")
    const fieldValidator = new RegExp("^\\w+")
    const valid = fieldValidator.test(data.title) && fieldValidator.test(data.description) && fieldValidator.test(data.content) && listValidator.test(formData.get("categories"));

    /* Send Data To backend */
    if (valid) {
      editPost(data, post.id)
        .then( res => { 
          alertSuccess("Success: Edited Post!");
          updateFeed(res.data);
          onClose();
        })
        .catch( err => { 
          console.log(err);
          alertError("Error: Could Not Edit Post!");
        });
    } else {
      alertError("Error: Must Fill In All Required Fields!");
    }

  }

return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md" sx={{borderRadius: "15px"}}>
        <DialogTitle>Edit post</DialogTitle>
        <DialogContent>
          <Box >
          <Box component="form" noValidate onSubmit={onSubmit}>
            <Grid container>
              <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                  <TextField
                    id="title"
                    label="Title"
                    multiline
                    maxRows={4}
                    sx={{width: "100%"}}
                    name = "title"
                    required
                    defaultValue={post.title}
                  />
                </Box>
              </Paper>
              <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                <TextField
                  id="description"
                  label="Description"
                  multiline
                  maxRows={4}
                  sx={{width: "100%"}}
                  name = "description"
                  defaultValue={post.description}
                  required
                />
                  </Box>
              </Paper>
              <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                  <TextField
                    id="content"
                    label="Content"
                    multiline
                    rows={6}
                    sx={{width: "100%"}}
                    name = "content"
                    defaultValue={post.content}
                    required
                  />
                  </Box>
              </Paper>
              <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                  <TextField
                    id="categories"
                    label="Categories"
                    fullWidth
                    name="categories"
                    defaultValue={post.categories.join(", ")}
                    required
                  />
                </Box>
              </Paper>
            </Grid>
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Finalize Edit?</Button>
          </Box>
          </Box>
          </DialogContent>
      </Dialog>
  );
}