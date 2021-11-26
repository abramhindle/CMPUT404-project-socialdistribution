import React from "react";
import { useHistory } from "react-router";
import "./components.css"
import MiniProfile from "./MiniProfile";

const InboxComment = ({ comment }) => {
  const history = useHistory();
  const goToPost = () => {
    console.log(comment.id.split("/"))
    history.push(`/author/${comment.id.split("/").at(-5)}/post/${comment.id.split("/").at(-3)}`)
  };
  return (
    <div className="itemContainer">
      <MiniProfile author={comment.author} /> <div className="likeText" onClick={goToPost}>commented on your post!</div>
    </div>
  );
}

export default InboxComment;