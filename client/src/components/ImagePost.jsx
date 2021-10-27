import React from "react";

const ImagePost = ({ post }) => {
  return (
    <img className="previewPic" alt='content_img' src={post.content} />
  )
};

export default ImagePost;