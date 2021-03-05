import React/*, { useEffect }*/ from 'react';

import Comment from '../components/Comments/Comment/Comment.js';

import { makeStyles } from '@material-ui/core/styles';


import simplifiedPosts from '../dummyData/Dummy.FeedPosts.js';

const useStyles = makeStyles(() => ({
    root: {
        minHeight: '200px',
        backgroundColor: 'white',
        marginBottom: '40px'
    },
}));  

export default function ExpandPost(props) {
    const classes = useStyles();
    
    // the id of the post would be obtained from the url, and used to fetch the full post with an API call.
    const authorId = props.match.params.authorId;
    const postId = props.match.params.postId;

    // console.log(postId)

    // Pretend this is an API call
    // const data = simplifiedPosts[0]
    const data = simplifiedPosts.find( post => post["id"] === `/author/${authorId}/posts/${postId}` )

    // const temp_comments = [
    //     {text: 'comment1'},
    //     {text: 'comment2'},
    //     {text: 'comment3'},
    //     {text: 'comment4'}
    // ];

    return (
        <div>
            <div className={classes.root}>
                <p>Post by: {data.author.displayName}</p>
                <p>Title: {data.title}</p>
                <p>Content: {data.content}</p>

                
            </div>
            {/* <Comments comments={temp_comments} /> */}

            {data.comments.map( comment => 
                <Comment 
                    key={comment.id}
                    comment={comment}
                />
            )}
        </div>
    )
}
