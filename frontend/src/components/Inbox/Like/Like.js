import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles(() => ({
    root: {
        // height: '300px',
        backgroundColor: 'white',
        marginBottom: '40px',
        borderRadius: "8px",
        padding: '1em 2em',
        display: 'flex'
    },
    summary: {
        marginTop: 'auto',
        marginBottom: 'auto'
    }
}));  


export default function Like(props) {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <p className={classes.summary}>{ props.data.summary }</p>
        </div>
    )
}
