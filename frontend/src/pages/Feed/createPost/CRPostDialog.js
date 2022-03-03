import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import Paper from '@mui/material/Paper';
import Dialog from '@mui/material/Dialog';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { createPost } from '../../../services/posts';
import FormHelperText from '@mui/material/FormHelperText';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormLabel from '@mui/material/FormLabel';



/*
 * Description: Detail view for each prize which allows user to purchase the prize
 */ 
export default function CRPostDialog(props) {


  const [content, setContent] = React.useState('');
  const [privacy, setPrivacy] = React.useState('');
  // const [unlisted, setUnlisted] = React.useState("");
  const handleChange = (event) => {
    setPrivacy(event.target.value);
  };
  const handleTextChange = (event) => {
    setContent(event.target.value);
  };
  

  const handleSubmit = (event) => {

    /* Grab Form Data */
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    if (formData.get("unlisted")=== "true"){
        formData.delete("unlisted")
        formData.append("unlisted", true)
    }else if(formData.get("unlisted")=== "false"){
        formData.delete("unlisted")
        formData.append("unlisted", false)
    }
    formData.append("contentType", content)
    formData.append("privacy", privacy)
    for (var pair of formData.entries()) {
      console.log(pair[0]+ ', ' + pair[1]); 
  }
  

      createPost(formData)
        /* Process Response */
        .then(res => {
            /* If Successful, Set The X-CSRFToken Value From The Response */
            console.log(res)
            if (res.status === 201) {
                console.log("Success Creating Post!")
                props.alertSuccess("Success: Created New Post!");
                props.onClose()
            }
        })
        .catch(err => {
            console.log("Failed to create post!")
            // props.handleOpenAlert("Failed To Add Prize!", "error")
            console.log(err)
        });
  };


return (

    
    <Dialog open={props.open} onClose={props.onClose} fullWidth maxWidth="md" sx={{borderRadius: "15px"}}>
        <DialogTitle>Creating Post</DialogTitle>
        <DialogContent>
          <Box >
          <Box component="form" noValidate onSubmit={handleSubmit}>
            <Grid container>
            <Paper sx={{width: "100%", mt:2}}>
                <Box sx={{width: "100%", p:1}}>
                <TextField
                  id="outlined-multiline-flexible"
                  label="Post Title"
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
                  id="outlined-multiline-flexible"
                  label="Post Description"
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
                    id="outlined-multiline-static"
                    label="Start Your Post from Here"
                    multiline
                    rows={6}
                    defaultValue="What I want to share today..."
                    sx={{width: "100%"}}
                    name = "content"
                    required
                  />
                  </Box>
              </Paper>


              <Grid container direction={'row'} spacing={1}>
                <Grid item xl={6} md={6} sm={12} xs={12}>
                  <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", pt:2, pl:1, height:"180px"}}>
                    <FormControl component="fieldset">
                    <FormLabel component="legend">List Setting</FormLabel>
                        <Paper sx={{p:1, m: 1, width: "390px", height:"120px", borderColor: '#000'}}>
                        <RadioGroup
                                aria-label="unlisted"
                                name="unlisted"
                                sx={{p:1}}
                            >
                            <FormControlLabel value= "true" control={<Radio /> } label="Unlisted"/>
                            <FormControlLabel value= "false" control={<Radio />} label="listed"/>
                        </RadioGroup>
                        </Paper>
                    </FormControl>
                    </Box>
                  </Paper>
                </Grid>
                <Grid item xl={6} md={6} sm={12} xs={12}>
                  <Paper sx={{width: "100%", mt:2}}>
                    <Box sx={{width: "100%", pt:2, pl:1,height:"180px"}}>
                    <FormControl required fullWidth>
                        <InputLabel id="demo-simple-select-label">Text Setting</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={content}
                        label="textSetting"
                        onChange={handleTextChange}
                        
                        >
                        <MenuItem value={"text/plain"}>Plain text Content type</MenuItem>
                        <MenuItem value={"text/markdown"}>Markdown Content type</MenuItem>
                        </Select>
                        <FormHelperText>Required</FormHelperText>
                    </FormControl>
                     <FormControl required fullWidth>
                        <InputLabel id="demo-simple-select-label">Visbility</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={privacy}
                        label="Visbility"
                        onChange={handleChange}
                        
                        >
                        <MenuItem value={"PRIVATE"}>Private Post</MenuItem>
                        <MenuItem value={"PUBLIC"}>Public Post</MenuItem>
                        <MenuItem value={"FRIENDS"}>Friends Only</MenuItem>
                        </Select>
                        <FormHelperText>Required</FormHelperText>
                    </FormControl>
                    </Box>
                  </Paper>
                </Grid>
            </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Post it now?
            </Button>
          </Box>
          </Box>
          </DialogContent>
      </Dialog>
    
  );
}