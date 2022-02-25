import * as React from 'react';
import {FormControl, MenuItem, InputLabel, DialogTitle, DialogContent, Dialog, Paper, TextField, Grid, Button, Box} from '@mui/material';
import Select from '@mui/material/Select';
import { createPost } from '../../../Services/posts';
import { useSelector } from 'react-redux';
import Card from '@mui/material/Card';
import CardMedia from '@mui/material/CardMedia';
import Collapse from '@mui/material/Collapse';



/*
 * Description: Detail view for each prize which allows user to purchase the prize
 */ 
export default function IMGPostDialog({alertSuccess, alertError, open, onClose, addToFeed}) {

  /* Hook For Post Content Type */
  const [content, setContent] = React.useState('image/png;base64');

  /* Hook For Post Visibility */
  const [privacy, setPrivacy] = React.useState('PUBLIC');

  /* Hook For User ID */
  const userID = useSelector( state => state.profile.url );

  /* Hook For Image URL */
  const [result, setResult] = React.useState('');

  /* Hook For Image Obj */
  const [image, setImage] = React.useState(null)

  /* Hook For Expand view */
  const [expanded, setExpanded] = React.useState(false);

  const handleExpandClick = () => {
        setExpanded(true);
      };
    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
          handleExpandClick()
          setImage(URL.createObjectURL(event.target.files[0]));
        }
       }

  const handleChange = (event) => {
    setPrivacy(event.target.value);
  };
  const handleTextChange = (event) => {
    setContent(event.target.value);
  };
  
  
//convert image to base 64
function getBase64(file) {
  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = function () {
    setResult(reader.result)
    console.log(reader.result);
  };
  reader.onerror = function (error) {
    console.log('Error: ', error);
  };
}
//https://stackoverflow.com/questions/36280818/how-to-convert-file-to-base64-in-javascript
//answered by Dmitri Pavlutin Mar 29, 2016 at 10:17
 


  /* This Function Posts Form Data To The Backend For Creating New Posts */
  const handleSubmit = (event) => {
    /* Grab Form Data */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const imageData = formData.get("content");
    console.log("result: ", imageData)
    getBase64(imageData);
    formData.append("IMGUrl", result)

    const data = {
      type: "post", 
      title: formData.get("title"), 
      description: formData.get("description"), 
      contentType: formData.get("contentType"), 
      content: formData.get("IMGUrl"), 
      categories: formData.get("categories").replaceAll(" ", "").split(","), 
      visibility: formData.get("visibility"), 
      unlisted: true
    }

    console.log("data content is: ", data.content)

    /* Validate Fields */
    const listValidator = new RegExp("^\\w+[,]?")
    const fieldValidator = new RegExp("^\\w+")
    const valid = fieldValidator.test(data.title) && fieldValidator.test(data.description) && listValidator.test(formData.get("categories"));

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
                        <MenuItem value={"image/png;base64"}>PNG</MenuItem>
                        <MenuItem value={"image/jpeg;base64"}>JPEG</MenuItem>
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
            <Paper sx={{p:1, mt:1}}>
            <Card fullWidth>
                        <Collapse in={expanded} timeout="auto" unmountOnExit>
                        <CardMedia
                            component="img"
                            height={image?image.clientHeight:0}
                            image={image}
                            alt="Preview"
                            sx={{borderRadius:2 }}
                        />
                        </Collapse>
                    </Card>
                    </Paper>
            <Button variant="contained" fullWidth onChange={onImageChange} component="label" sx={{ mt: "25px"}}>Upload Image<input type="file" name="content" id="content" hidden  /></Button>
            <Button type="submit" fullWidth variant="contained" sx={{ my: "15px" }}>Post it now?</Button>
          </Box>
          </Box>
          </DialogContent>
      </Dialog>
  );
}