import React from 'react'
import PlainPost from '../../components/Posts/post-plain'
import './post-list.css';

function PostList({user_list}) { //gets a json object, and returns a list item for it
    
    return (
        <div className='posts'>
            <ul className='postsList'>
                {console.log(user_list)}
                {user_list.items.map((list_item) => <li className='post' key={list_item.id}> <PlainPost post={list_item}/> </li>)};
            </ul>
        </div>
        );
}   

export default PostList;