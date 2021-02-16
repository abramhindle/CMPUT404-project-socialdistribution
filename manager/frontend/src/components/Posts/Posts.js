import React from 'react';

import Post from './Post/Post';

export default function Posts(props) {
    let posts = props.posts.map((d, i) => <Post key={i} postContent={d.title}/>);

    return (
        <div>
            {posts}
        </div>
    )
}
