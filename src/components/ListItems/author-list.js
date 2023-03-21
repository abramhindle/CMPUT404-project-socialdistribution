import React from 'react'
import './author-list.css';

function AuthorList({user_list}) { //gets a json object, and returns a list item for it
   

    const formatFollowerList = (author) =>{
        const port = window.location.port ? `:${window.location.port}` : "";
        const authorUrl = `//${window.location.hostname}${port}/user/${(author.id ?? "").split('/').pop()}`; // allows linking to the author who wrote the post

        return (
            <div className='follower'>
                <h6><a href={authorUrl}>{author.displayName}</a></h6>
                {<img alt="author" src={author.profileImage}></img>}
            </div>
        );
    };

    return (
    <div className='followersList'>
        <ul className='followers'>
            {user_list.items.map((list_item) => <li className='follower' key={list_item.id}> {formatFollowerList(list_item)} </li>)};
        </ul>
    </div>
    );
}   

export default AuthorList;