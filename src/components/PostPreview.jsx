import { useHistory } from 'react-router';
import React from 'react';
import MiniProfile from './MiniProfile';
import { Card } from '@mui/material';
import './components.css';

const PostPreview = ({ post }) => {
  const history = useHistory();

  const goToPost = (postID, authorID) => {
    postID = postID.split('/').at(-1);
    authorID = authorID.split('/').at(-1);

    history.push(`/author/${authorID}/post/${postID}`);
  };

  const muiOverride = {
    border: '1px solid #c4c4c4',
    transition: 'border 500ms ease'
  };
  return (
    <Card
      variant='outlined'
      sx = {muiOverride}
      className='postPreviewContainer'
      onClick={() => {
          goToPost(post.id, post.author.id);
        }}>
        <MiniProfile author={post.author} />
        <div className='postPreviewHeader'>Title</div>
        <div className='postPreviewTitle'>{post.title}</div>
        <div className='postPreviewHeader'>Description</div>
        <div className='postPreviewDescription'>{post.description}</div>
    </Card>
  );
};

export default PostPreview;
