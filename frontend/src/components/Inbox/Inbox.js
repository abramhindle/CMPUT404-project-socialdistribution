import React, { useEffect, useState } from 'react';

import Post from './Post/Post';
import FollowRequest from './FollowRequest/FollowRequest';

export default function Inbox(props) {
    const inbox = props.data.items !== undefined
        ? props.data.items.map((d, i) => {
            if (d.type === 'Follow') {
                return <FollowRequest key={i} request={d}/>
            } else {
                return <Post key={i} postData={d}/>;
            }
        })
        : null;
    return (
        <div>
            {inbox}
        </div>
    )
}
