import React from 'react';

import Comment from './Comment/Comment';

export default function Comments(props) {
    let comments = props.comments.map((d, i) => <Comment key={i} comment={d}/>);

    return (
        <div>
            {comments}
        </div>
    )
}
