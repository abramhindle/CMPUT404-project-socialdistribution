import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import Post from "../components/Post";
import Comment from "../components/Comment";
import postService from "../services/post";

const ViewPost = () => {
  const { authorID, postID } = useParams();
  const [ comments, setComments ] = useState([]);
  const [ post, setPost ] = useState([]);

  useEffect(() => {
    const getPost = async () => {
      const response = await postService.getPost(authorID, postID);
      const likeRes = await postService.getLikes(authorID, postID);
      setPost({ ...response.data, likes: likeRes.data.items });
    };

    const getComments = async () => {
      const response = await postService.getComments(authorID, postID, 1, 5);
      setComments(response.data.items.map(async (comment) => {
        const likeRes = await postService.getCommentLikes(authorID, postID, comment.id.split('/').at(-1))
        return { ...comment, likes: likeRes.data.items }
      }));
    };  

    getPost();
    getComments();
  }, [ authorID, postID ]);

  return (
    <div>
      <Post post={post} />
      { comments.map((comment) => <Comment comment={comment} />)};
    </div>  
  );
}

export default ViewPost;