import { useHistory } from 'react-router';
import React from 'react';
import "./components.css";
import MiniProfile from './MiniProfile';

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
      <MiniProfile author={post.author} />
      <div className="postPreviewHeader">Title</div>
      <div className="postPreviewTitle">{post.title}</div>
      <div className="postPreviewHeader">Description</div>
      <div className="postPreviewDescription">{post.description}</div>
    </div>
  )
};

export default PostPreview;