import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        height: '200px',
        backgroundColor: 'white',
        marginBottom: '40px'
    },
  }));  


export default function Post(props) {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            {props.postContent}
        </div>
    )
}
