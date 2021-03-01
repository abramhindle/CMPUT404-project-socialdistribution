import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
// import Link from '@material-ui/core/Link';

import { Link } from 'react-router-dom'

const useStyles = makeStyles(() => ({
    root: {
        minHeight: '200px',
        backgroundColor: 'white',
        marginBottom: '40px'
    },
  }));  


export default function Post(props) {
    const classes = useStyles();
    
    // const { history } = props;
    const { postData } = props;

    // click on the Comments count to see the full post, with its paginated comments
    // const handleSeeFullPost = (url) => {
    //     // can't use history because Post is not a Route, so that prop is unavailable
    //     history.push(url)
    // }

    return (
        <div className={classes.root}>
            <p>Post by: {postData.author.displayName}</p>
            <p>Title: {postData.title}</p>
            <p>Content: {postData.content}</p>

            {/* To see the full post with paginated comments, I think it should be a link, but I get the 404 because of Django */}
            <Link 
                target="_blank" 
                to={`http://localhost:8000/${postData.id}`}
            >
                {`Comments (${postData.count})`}
            </Link>
            {/* <a 
                // onClick={handleSeeFullPost(postData.id)}
                // href={`http://localhost:8000/${postData.id}`}
            >
                {`Comments (${postData.count})`}
            </a> */}

        </div>
    )
}
