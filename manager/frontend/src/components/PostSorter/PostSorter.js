import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        margin: '40px 0px'
    },
  }));  

export default function PostSorter() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <hr />
        </div>
    )
}
