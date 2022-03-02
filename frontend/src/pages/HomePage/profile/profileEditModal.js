import * as React from 'react';
import { Modal, Typography, Box, Button, TextField, Stack, Container, Grid } from '@mui/material';
import { styled } from '@mui/material/styles';
import Badge from '@mui/material/Badge';
import Avatar from '@mui/material/Avatar';
import AddCircleSharpIcon from '@mui/icons-material/AddCircleSharp';
import { useSelector, useDispatch } from 'react-redux';
import axios from 'axios';

const style = {
    textField: { minWidth: '20rem' },
    box: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        minWidth: '40rem',
        minHeight: '20vh',
        bgcolor: 'background.paper',
        boxShadow: 24,
        p: 4,
    },
    avatar: {
        width: 70,
        height: 70
    },
    addIcon: {
        width: 30,
        height: 30,
        fill: 'green'
    },
    buttonContainer: {
        marginTop: '2rem',
        marginLeft: 'auto'
    }
};

const SmallAvatar = styled(Avatar)(({ theme }) => ({
    width: 30,
    height: 30,
    border: `2px solid ${theme.palette.background.paper}`,
}));

export default function ProfileEditModal(props) {
    const profileImage = useSelector(state => state.profile.profileImage);
    const github = useSelector(state => state.profile.github);
    const dispatch = useDispatch();
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

    };

    return (
        <Modal
            open={props.isOpen}
            onClose={props.onClose}
            aria-labelledby="modal-profile-edit"
            aria-describedby="modal-profile-editing"
        >
            <Box sx={style.box}>
                <Typography sx={{ fontWeight: 'bold', marginBottom: '2rem' }} id="modal-modal-title" variant="h4" component="h2">
                    Edit Profile
                </Typography>

                <Grid container spacing={0} justifyContent="center" direction='row' alignItems='center'>
                    <Grid item xs={3} onClick={() => console.log(11)}><Badge
                        overlap="circular"
                        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
                        badgeContent={
                            // <SmallAvatar alt="d" src={AddIcon} />
                            <AddCircleSharpIcon sx={style.addIcon} />
                        }
                    >
                        <Avatar alt="Travis Howard" src={profileImage} sx={style.avatar} />
                    </Badge></Grid>

                    <Grid item xs={9} component="form" noValidate onSubmit={handleSubmit}>
                        <TextField
                            id="outlined"
                            name="github"
                            label="Github Link"
                            defaultValue={github}
                            sx={style.textField}
                        />
                    </Grid>
                </Grid >


                <Stack spacing={1} sx={style.buttonContainer}>
                    <Button variant='contained'>Save</Button>
                    <Button variant='outlined'>Cancel</Button>
                </Stack>

            </Box >
        </Modal >
    )
}