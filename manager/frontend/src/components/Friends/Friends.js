import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import Friend from './Friend/Friend';

const useStyles = makeStyles(() => ({
    root: {
      backgroundColor: "white",
      marginBottom: "30px"
    },
  }));  

export default function Friends(props) {
    const classes = useStyles();

    let posts = props.friends.map((d, i) => <Friend key={i} friend={d}/>);

    return (
        <div className={classes.root}>
            {posts}
        </div>
    )
}
