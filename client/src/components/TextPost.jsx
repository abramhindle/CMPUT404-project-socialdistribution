import React from "react"
import { Parser, HtmlRenderer } from "commonmark";

const TextPost = ({ post }) => {
  const reader = Parser();
  const writer = HtmlRenderer();

  return (
    <>{
      post.contentType === "text/plain" ? 
        <p>{post.content}</p> 
      : writer.render(reader.parse(post.content)) 
    }</>
  );
}

export default TextPost;