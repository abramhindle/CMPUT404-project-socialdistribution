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

const Post = ({ post, setPost }) => {
  const { user } = useContext(UserContext);
  const [ editing, setEditing ] = useState(false);
  const history = useHistory();

  const onSubmit = async (postData) => {
    try {
      const response = await authorService.getAuthor(user.author.authorID);
      console.log(response.data)
      postData.author = response.data;
      console.log(postData)
      const updateResponse = await postService.updatePost(
        jsCookies.getItem('csrftoken'),
        user.author.authorID,
        post.id.split("/").at(-1),
        postData
      );
      setPost(updateResponse.data)
      setEditing(false);
      console.log(updateResponse)
    } catch (e) {
      console.log(e);
      alert('Error editing post');
    }
  };

  const onEdit = () => { setEditing(!editing); }
  const onDelete = async () => {
    try {
      await postService.removePost(jsCookies.getItem("csrftoken"), user.author.authorID, post.id.split("/").at(-1))
      history.push("/")
    } catch (e) {
      console.log(e);
      alert('Error deleting post');
    }
   }
   const onLike = async () => {
    try {
      const authorResponse = await authorService.getAuthor(user.author.authorID);
      const response = await postService.likePost(jsCookies.getItem('csrftoken'), user.author.authorID, { author: authorResponse.data, object: post.id })
      setPost({ ...post, likes: post.likes.concat(response.data)})
      console.log(response)
    } catch (e) {
      console.log(e.response.status);
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
        <h2>{post.title}</h2>
        { post.contentType === "image/jpeg;base64" || post.contentType === "image/png;base64" ?
            <ImagePost post={post} />
            : post.contentType === "application/base64" ?
            <AttachmentPost post={post} />
            : post.contentType === "text/plain" || post.contentType === "text/markdown" ?
            <TextPost post={post} />
            : <p>o.o</p>
        }
        <div><button onClick={onLike}>👍 {post.likes.length}</button>
        { editing === false && post.author.id.split("/").at(-1) === user.author.authorID ?
          <>
            <button onClick={onEdit}>✏️ Edit </button> 
            <button onClick={onDelete}>❌ Delete </button>
          </>
        : <></>}
        </div>
      </div>
      : <PostEdit post={post} setPost={setPost} onSubmit={onSubmit}/> 
    } </div>
  );
};

export default Post;