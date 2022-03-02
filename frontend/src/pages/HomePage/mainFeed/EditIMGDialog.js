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
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';

export default function EditPostDialog({post, alertSuccess, alertError, open, onClose, updateFeed}) {
  /* Hook For Post Unlisted */
  const [unlisted, setUnlisted] = React.useState(false);
  /* Hook For Image Obj */
  const [image, setImage] = React.useState(post.content)

  const onImageChange = (event) => {
    if (event.target.files && event.target.files[0]) {
      setImage(URL.createObjectURL(event.target.files[0]));
    }
   }

  const handleUnlistedChange = (event) => {
    setUnlisted(event.target.value);
  };


  const onSubmit = (event) => {
    /* Grab Data From Form */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const imageData = formData.get("content");
    const reader = new FileReader();
    reader.readAsDataURL(imageData)
    reader.onload = () => { 
      const data = {
        type: "post", 
        title: formData.get("title"), 
        description: formData.get("description"), 
        contentType: post.contentType, 
        content: reader.result, 
        categories: formData.get("categories").replaceAll(" ", "").split(","), 
        visibility: post.visibility, 
        unlisted: formData.get("unlisted")
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
                <Box sx={{width: "100px", p:1}}>
                  <img src={image} width="1000%" alt={post.title}/>
                  </Box>
              </Paper>
              <Grid container direction={'row'} spacing={1}>
                <Grid item xl={6} md={6} sm={12} xs={12}>
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
                <Grid item xl={6} md={6} sm={12} xs={12}>
                  <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", p:"8px"}}>
                     <FormControl required fullWidth>
                        <InputLabel id="unlisted">Unlisted</InputLabel>
                        <Select
                          labelId="unlisted"
                          id="unlisted"
                          name="unlisted"
                          defaultValue={post.unlisted}
                          label="unlisted"
                          onChange={handleUnlistedChange}
                        >
                        <MenuItem value={true}>True</MenuItem>
                        <MenuItem value={false}>False</MenuItem>
                        </Select>
                    </FormControl>
                    </Box>
                  </Paper>
                </Grid>
              </Grid>
            </Grid>
            <Button variant="contained" fullWidth onChange={onImageChange} component="label" sx={{ mt: "25px"}}>Upload Image<input type="file" name="content" id="content" hidden  /></Button>
            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Finalize Edit?</Button>
          </Box>
          </Box>
          </DialogContent>
      </Dialog>
  );
}