import React, { useEffect, useState } from 'react';

import Post from '../Post/Post';

export default function Stream(props) {
    const inbox = props.data !== undefined
        ? props.data.map((d, i) => {
            if (d.type === 'post') {
                return <Post
                            key={i}
                            postData={d}
                            author={props.author}
                            createComment={props.createComment}
                            sharePost={props.sharePost}
                            editMode={true}
                            deleteClicked={props.deleteClicked}
                            editPost={props.editPost}
                            comments={props.comments[d.id]}
                            postLiked={props.postLiked}
                            commentLiked={props.commentLiked}
                        />;
            }
        })
        : null;
    
    return (
        <div>
            {inbox}
        </div>
    );
}
