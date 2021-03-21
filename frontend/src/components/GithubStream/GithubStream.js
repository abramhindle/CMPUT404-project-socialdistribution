import React from 'react';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        height: '300px',
        backgroundColor: 'white',
        marginBottom: '40px',
        borderRadius: "8px",
    }
}));

export default function GithubStream() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            
        </div>
    )
}
