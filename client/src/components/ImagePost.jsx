import React from "react";

const ImagePost = ({ post }) => {
  return (
    <img src={`data:${post.contentType}, ${post.content}`} alt={post.title} />
  );
}

export default ImagePost;