import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        minHeight: '200px',
        backgroundColor: 'white',
        marginBottom: '40px'
    },
  }));  


export default function Post({ postData }) {
    const classes = useStyles();
    return (
        <div className={classes.root}>
            <p>Post by: {postData.author.displayName}</p>
            <p>Title: {postData.title}</p>
            <p>Content: {postData.content}</p>
            <p>{`Comments (${postData.count})`}</p>

        </div>
    )
}
