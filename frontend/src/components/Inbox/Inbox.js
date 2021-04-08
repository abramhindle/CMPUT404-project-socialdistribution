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
                return <Post
                            key={i}
                            postData={d}
                            onLikeClicked={props.postLiked}
                            author={props.author}
                            createComment={props.createComment}
                            getLikes={props.getLikes}
                            sharePost={props.sharePost}
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
