import React, { useEffect, useState } from 'react';

import Post from '../Post/Post';
import FollowRequest from './FollowRequest/FollowRequest';
import Like from './Like/Like';

export default function Inbox(props) {
    const inbox = props.data.items !== undefined
        ? props.data.items.map((d, i) => {
            if (d.type === 'Follow') {
                return <FollowRequest key={i} request={d} author={props.author} postFriendRequest={props.postFriendRequest}/>;
            } else if (d.type === 'post') {
                const conversion = d.id.split('/');
                conversion[5] = 'post'
                return <Post
                            key={i}
                            postData={d}
                            postLiked={props.postLiked}
                            commentLiked={props.commentLiked}
                            author={props.author}
                            createComment={props.createComment}
                            sharePost={props.sharePost}
                            editMode={false}
                            likes={props.likes[conversion.join('/')]}
                            comments={props.comments[d.id]}
                        />;
            } else if (d.type === 'like') {
                return <Like key={i} data={d}/>;
            }
        })
        : null;
    
    return (
        <div>
            {inbox}
        </div>
    );
}
