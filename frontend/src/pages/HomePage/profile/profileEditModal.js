import * as React from 'react'
import { Modal, Typography, Box, Button, TextField, Stack } from '@mui/material'

const style = {
    textField: { width: '25rem' },
    box: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: '50vw',
        minHeight: '50vh',
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
    },

};

export default function ProfileEditModal(props) {
    return (
        <Modal
            open={props.isOpen}
            onClose={props.onClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style.box}>

                <Stack direction="column" spacing={5}>
                    <Typography sx={{ fontWeight: 'bold' }} id="modal-modal-title" variant="h4" component="h2">
                        Edit Profile
                    </Typography>
                    <TextField
                        required
                        id="outlined-required"
                        label="Display Name"
                        defaultValue="Abigail Kindle"
                        sx={style.textField}
                    />
                    <TextField
                        disabled
                        sx={style.textField}
                        id="outlined-required"
                        label="Username"
                        defaultValue="abkin"
                    />
                </Stack>


                <Typography id="modal-modal-description" sx={{ mt: 2 }}>
                    Duis mollis, est non commodo luctus, nisi erat porttitor ligula.
                </Typography>
            </Box>
        </Modal>
    )
}