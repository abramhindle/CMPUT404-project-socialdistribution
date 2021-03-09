import React, { useEffect, useState } from 'react';

import Post from './Post/Post';

export default function Posts(props) {
    let posts = props.postData.map((d, i) => <Post key={i} postData={d}/>);
    return (
        <div>
            { posts }
        </div>
    )
}
