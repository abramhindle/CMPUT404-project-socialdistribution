import React, { useContext, useState } from "react";
import ImagePost from "./ImagePost";
import AttachmentPost from "./AttachmentPost";
import TextPost from "./TextPost";
import { UserContext } from "../UserContext";
import PostEdit from "./PostEdit"
import authorService from "../services/author";
import postService from "../services/post";
import jsCookies from "js-cookies";
import { useHistory } from "react-router";
import MiniProfile from "./MiniProfile";

const Post = ({ post, setPost }) => {
  const { user } = useContext(UserContext);
  const [ editing, setEditing ] = useState(false);
  const history = useHistory();

  const onSubmit = async (postData) => {
    try {
      const response = await authorService.getAuthor(user.author.authorID);
      postData.author = response.data;
      const updateResponse = await postService.updatePost(
        jsCookies.getItem('csrftoken'),
        user.author.authorID,
        post.id.split("/").at(-1),
        postData
      );
      setPost(updateResponse.data)
      setEditing(false);
    } catch (e) {
      alert('Error editing post');
    }
  };

  const onEdit = () => { setEditing(!editing); }

  const onShare = async () => {
    try {
      const response = await authorService.getAuthor(user.author.authorID);
      await postService.createPost(
        jsCookies.getItem("csrftoken"), 
        user.author.authorID,
        { ...post, author: response.data } 
      )
    } catch (e) {
      alert('Error editing post');
    }
  }

  const onDelete = async () => {
    try {
      await postService.removePost(jsCookies.getItem("csrftoken"), user.author.authorID, post.id.split("/").at(-1))
      history.push("/")
    } catch (e) {
      alert('Error deleting post');
    }
   }
   const onLike = async () => {
    try {
      const authorResponse = await authorService.getAuthor(user.author.authorID);
      const response = await postService.likePost(jsCookies.getItem('csrftoken'), post.author.id.split("/").at(-1), { author: authorResponse.data, object: post.id })
      setPost({ ...post, likes: post.likes.concat(response.data)})
    } catch (e) {
      if (e.response?.status === 409) {
        alert('You have already liked this post');
      } else {
        console.log(e);
      }
    }
   }

  return (
    <div> { editing === false ?
      <div>
        <MiniProfile author={post.author} /> 
        <h2 className="postTitle">{post.title}</h2>
        { post.contentType === "image/jpeg;base64" || post.contentType === "image/png;base64" ?
            <ImagePost post={post} />
            : post.contentType === "application/base64" ?
            <AttachmentPost post={post} />
            : post.contentType === "text/plain" || post.contentType === "text/markdown" ?
            <TextPost post={post} />
            : <p>o.o</p>
        }
        <div className="postButtonContainer"><div className="postButton" onClick={onLike}>Like ({post?.likes?.length})</div>
          <div className="postButton" onClick={onShare}>Share</div>
        { editing === false && post.author.id.split("/").at(-1) === user.author.authorID ?
          <>
            <div className="postButton" onClick={onEdit}>Edit </div> 
            <div className="postButton" onClick={onDelete}> Delete </div>
          </>
        : <></>}
        </div>
      </div>
      : <PostEdit post={post} setPost={setPost} onSubmit={onSubmit}/> 
    } </div>
  );
};

export default Post;