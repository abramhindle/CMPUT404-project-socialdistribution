import React from 'react';

import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles(() => ({
    root: {
        // height: '300px',
        backgroundColor: 'white',
        marginBottom: '40px',
        borderRadius: "8px",
        padding: '1em 2em'
    },
}));  


export default function FollowRequest(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            { props.request.summary }
        </div>
    )
}
