import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        height: '200px',
        backgroundColor: 'lightgray'
    },
  }));  

export default function PostCreator() {
    const classes = useStyles();

    return (
        <div
            className={classes.root}
        >
            Create new post
        </div>
    )
}
