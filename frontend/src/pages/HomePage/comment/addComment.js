import * as React from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

export default function addComments() {

    

  return (
    <Box
      component="form"
      noValidate
      autoComplete="off"
      sx={{p:"2%"}}
    >
        <Stack spacing={2} direction="row">
            <TextField
                id="outlined-textarea"
                label="Add Comment Here"
                placeholder="Add Comment Here"
                multiline
                sx={{width: "83%"}}
                />

            <Button variant="contained">Add Comment</Button>
        </Stack>
    </Box>
  );
}