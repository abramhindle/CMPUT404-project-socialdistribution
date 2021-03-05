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

            {/* To see the full post with paginated comments, I think it should be a link, but I get the 404 because of Django */}
            {/* <Link 
                target="_blank" 
                // to={`http://localhost:8000/${postData.id}`}
                to={`${postData.id}`}
            >
                {`Comments (${postData.count})`}
            </Link> */}
            <a 
                onClick={() => handleSeeFullPost(postData.id)}
                // href={`${postData.id}`}
                // href="http://localhost:8000/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            >
                {`Comments (${postData.count})`}
            </a>

            {/* <Redirect 
                // to={postData.id}  
                to="/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e"
            >
                {`Comments (${postData.count})`}
            </Redirect> */}

        </div>
    )
}
