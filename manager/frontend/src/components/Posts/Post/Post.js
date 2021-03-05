import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
// import Link from '@material-ui/core/Link';

// import { Link, Redirect } from 'react-router-dom'

const useStyles = makeStyles(() => ({
    root: {
        minHeight: '200px',
        backgroundColor: 'white',
        marginBottom: '40px'
    },
  }));  


export default function Post(props) {
    const classes = useStyles();
    
    const { history } = props;
    const { postData } = props;

    // click on the Comments count to see the full post, with its paginated comments
    const handleSeeFullPost = (url) => {
        history.push(url)
    }

    // console.log(postData.id)

    return (
        <div className={classes.root}>
            <p>Post by: {postData.author.displayName}</p>
            <p>Title: {postData.title}</p>
            <p>Content: {postData.content}</p>

            <a 
                onClick={() => handleSeeFullPost(postData.id)}
            >
                {`Comments (${postData.count})`}
            </a>
        </div>
    )
}
