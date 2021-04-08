import React, { useEffect, useState } from 'react';

import Post from '../Post/Post';

export default function Stream(props) {
    console.log(props);
    const inbox = props.data !== undefined
        ? props.data.map((d, i) => {
            if (d.type === 'post') {
                return <Post
                            key={i}
                            postData={d}
                            onLikeClicked={() => {}}
                            author={props.author}
                            createComment={() => {}}
                            getLikes={() => {}}
                            sharePost={() => {}}
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
