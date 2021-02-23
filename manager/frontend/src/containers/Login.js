import React from 'react';
import { Link } from 'react-router';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';

const useStyles = makeStyles(() => ({
    root: {
    },
    logo: {
        height: '150px',
        width: '150px',
        backgroundColor: '#D1305E',
        borderRadius: '10px',
        margin: '40px auto'
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
    links: {
        margin: '1em 0'
    }
  }));  

export default function Login() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <div className={classes.logo}>
            </div>
            <h2 className={classes.title}>Welcome Back</h2>
            <div className={classes.text}>
                <div className={classes.textField}>
                    <TextField id="standard-basic" label="Username"/>
                    <TextField id="standard-basic" label="Password" type="password"/>
                    <div className={classes.links}>
                        <a href="/">Sign Up</a>
                        <a href="/" className={[classes.passwordRecover, 'test'].join(' ')}>Forgot your password?</a>
                    </div>
                </div>
            </div>
        </div>
    )
}
