import React from 'react';
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
    }
  }));  

export default function Login() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <div className={classes.logo}>
            </div>
            <h2 className={classes.title}>Welcome Back</h2>
            <div>
                <TextField id="standard-basic" label="Username" />
            </div>
            <div>
                <TextField id="standard-basic" label="Password" type="password"/>
            </div>
        </div>
    )
}
