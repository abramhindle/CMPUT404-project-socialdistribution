import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';


export default function urlSharingBox({post}) {

 console.log("LOLOLOL")

  return (
      
    <Box sx={{pl:3}}>
        <TextField
          disabled
          id="outlined-disabled"
          defaultValue={post.id}
          sx={{width: "75%"}}
        />
        <Button sx={{ml:1, width: "20%", height:55}} variant="outlined" startIcon={<ContentCopyIcon />} onClick={() =>  navigator.clipboard.writeText(post.id)}>
        Copy
      </Button>
    
    </Box>
  );
}