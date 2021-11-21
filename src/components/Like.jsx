import React from "react";
import "./components.css"
import MiniProfile from "./MiniProfile";

const Like = ({ like }) => {
  return (
    <div className="itemContainer">
      <MiniProfile author={like.author} /> <div className="likeText">liked your post</div>
    </div>
  );
}

export default Like;