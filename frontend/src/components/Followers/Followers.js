import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        backgroundColor: 'white'
    },
  }));  

export default function Followers(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            You have {props.followerCount} followers
        </div>
    )
}
