import React from 'react';
import { Link } from 'react-router';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(() => ({
    root: {
    },
    logo: {
        height: '150px',
        width: '150px',
        backgroundColor: '#D1305E',
        borderRadius: '10px',
        margin: '40px auto',
    },
    title: {
        textAlign: 'center'
    },
    text: {
        display: 'flex',
        alignContent: 'center',
        justifyContent: 'center',
    },
    textField: {
        display: 'flex',
        flexDirection: 'column',
        width: '30em'
    },
    passwordRecover: {
        float: 'right'
    },
    register: {
        width: '10em',
        margin: '2em auto',
        backgroundColor: '#D1305E',
        fontWeight: '300',
        fontSize: '0.8em',
        textTransform: 'none'
    }
}));

export default function Signup() {
    const classes = useStyles();

    const registerClicked = () => {
        console.log('register clicked');
    }

    return (
        <div className={classes.root}>
            <div className={classes.logo}>
            </div>
            <h2 className={classes.title}>Sign up for a free account</h2>
            <div className={classes.text}>
                <div className={classes.textField}>
                    <TextField id="standard-basic" label="Username"/>
                    <TextField id="standard-basic" label="Password" type="password"/>
                    <TextField id="standard-basic" label="Re-enter Password" type="password"/>
                    <Button className={classes.register} variant="contained" color="secondary" onClick={registerClicked}> 
                        Register
                    </Button>
                </div>
            </div>
        </div>
    )
}
