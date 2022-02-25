import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { createPost } from '../../../services/posts';
import { useSelector } from 'react-redux';



/*
 * Description: Detail view for each prize which allows user to purchase the prize
 */ 
export default function CRPostDialog({alertSuccess, alertError, open, onClose, addToFeed}) {

  /* Hook For Post Content Type */
  const [content, setContent] = React.useState('text/plain');

  /* Hook For Post Visibility */
  const [privacy, setPrivacy] = React.useState('PUBLIC');

  /* Hook For User ID */
  const userID = useSelector( state => state.profile.url );

  const handleChange = (event) => {
    setPrivacy(event.target.value);
  };
  const handleTextChange = (event) => {
    setContent(event.target.value);
  };

  /* This Function Posts Form Data To The Backend For Creating New Posts */
  const handleSubmit = (event) => {
    /* Grab Form Data */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const data = {
      type: "post", 
      title: formData.get("title"), 
      description: formData.get("description"), 
      contentType: formData.get("contentType"), 
      content: formData.get("content"), 
      categories: formData.get("categories").replaceAll(" ", "").split(","), 
      visibility: formData.get("visibility"), 
      unlisted: false
    }

    /* Validate Fields */
    const listValidator = new RegExp("^\\w+[,]?")
    const fieldValidator = new RegExp("^\\w+")
    const valid = fieldValidator.test(data.title) && fieldValidator.test(data.description) && fieldValidator.test(data.content) && listValidator.test(formData.get("categories"));

    /* Send Data To backend */
    if (valid) {
      console.log(data);
      createPost(data, userID)
        .then( res => { 
          alertSuccess("Success: Created New Post!");
          addToFeed(res.data);
          onClose();
        })
        .catch( err => { 
          console.log(err);
          alertError("Error: Could Not Create Post!");
        });
    } else {
      alertError("Error: Must Fill In All Required Fields!");
    }
  };

return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="md" sx={{borderRadius: "15px"}}>
        <DialogTitle>Creating Post</DialogTitle>
        <DialogContent>
          <Box >
          <Box component="form" noValidate onSubmit={handleSubmit}>
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
                    required
                  />
                </Box>
              </Paper>
              <Grid container direction={'row'} spacing={1}>
                <Grid item xl={6} md={6} sm={12} xs={12}>
                  <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", p:"6px"}}>
                    <FormControl required fullWidth>
                        <InputLabel id="contentType">Content Type</InputLabel>
                        <Select
                          labelId="contentType"
                          id="contentType"
                          name="contentType"
                          value={content}
                          label="Content Type"
                          onChange={handleTextChange}
                        >
                        <MenuItem value={"text/plain"}>Plain Text</MenuItem>
                        <MenuItem value={"text/markdown"}>Markdown</MenuItem>
                        </Select>
                    </FormControl>
                    </Box>
                  </Paper>
                </Grid>
                <Grid item xl={6} md={6} sm={12} xs={12}>
                  <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", p:"6px"}}>
                     <FormControl required fullWidth>
                        <InputLabel id="visibility">Visbility</InputLabel>
                        <Select
                          labelId="visibility"
                          id="visibility"
                          name="visibility"
                          value={privacy}
                          label="Visbility"
                          onChange={handleChange}
                        >
                        <MenuItem value={"PUBLIC"}>Public Post</MenuItem>
                        <MenuItem value={"FRIENDS"}>Friends Only</MenuItem>
                        </Select>
                    </FormControl>
                    </Box>
                  </Paper>
                </Grid>
            </Grid>
            </Grid>
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}> Post it now?</Button>
          </Box>
          </Box>
          </DialogContent>
      </Dialog>
  );
}