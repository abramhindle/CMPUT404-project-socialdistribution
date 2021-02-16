import React from 'react';

import Post from '../components/Posts/Post/Post';
import Comments from '../components/Comments/Comments';

export default function ExpandPost(props) {
    const temp_comments = [
        {text: 'comment1'},
        {text: 'comment2'},
        {text: 'comment3'},
        {text: 'comment4'}
    ];

    return (
        <div>
            <Post postContent='post1'/>
            <Comments comments={temp_comments} />
        </div>
    )
}
