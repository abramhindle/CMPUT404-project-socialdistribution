import React from 'react'

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        margin: '10px 10px',
        '&:hover': {
            backgroundColor: '#D3D3D3',
        }
    },
}));  

export default function Friend(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            {props.friend.displayName}
        </div>
    )
}
