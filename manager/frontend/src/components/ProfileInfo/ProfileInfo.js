import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        height: '200px',
        backgroundColor: 'white'
    },
  }));

export default function ProfileInfo(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            Your Name: {props.profile.name}
        </div>
    )
}
