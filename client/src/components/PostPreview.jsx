import { useHistory } from 'react-router';
import React from 'react';
import "./components.css";

const PostPreview = ({ post }) => {
  const history = useHistory();

  const goToPost = (postID, authorID) => {
    postID = postID.split('/').at(-1);
    authorID = authorID.split('/').at(-1);

    history.push(`/author/${authorID}/post/${postID}`);
  };

  return(
    <div
      className='postPreviewContainer'
      onClick={() => {
        goToPost(post.id, post.author.id);
      }}
    >
      <p>Title: {post.title}</p>
      <p>Description: {post.description}</p>
      <p>Author: {post.author.displayName}</p>
    </div>
  )
};

export default PostPreview;