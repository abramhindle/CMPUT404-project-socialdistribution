import React from "react";
import ImagePost from "./ImagePost";
import AttachmentPost from "./AttachmentPost";
import TextPost from "./TextPost";

const Post = ({ post }) => {
    return (
        <div> 
            <h2>{post.title}</h2>
            {
                post.contentType === "image/jpeg;base64" || post.contentType === "image/png;base64" ?
                    <ImagePost post={post} />
                : post.contentType === "application/base64" ?
                    <AttachmentPost post={post} />
                : post.contentType === "text/plain" || post.contentType === "text/markdown" ?
                    <TextPost post={post} />
                : <p>o.o</p>
            }
        </div>
    );
};

export default Post;