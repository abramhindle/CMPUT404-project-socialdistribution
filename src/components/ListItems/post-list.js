import "./post-list.css";
import DisplayItem from "../Posts/display";
import React, { useEffect, useState } from "react";
import { get_liked } from "../../api/like_api";
import { useSelector } from "react-redux";

function PostList({ user_list }) {
  //gets a json object, and returns a list item for it
  const [liked, setLiked] = useState([]);
  const user = useSelector((state) => state.user);

  useEffect(() => {
    get_liked(user.id, setLiked);
  }, []);

  function checkLiked(item) {
    for (var i = 0; i < liked.length; i++) {
      if (liked[i].object === item.id) {
        //console.log("liked", liked[i].object, item.id)
        return true;
      }
    }
    return false;
  }

  return (
    <div className="posts">
      <ul className="postsList">
        {console.log(user_list)}
        {user_list.items.map((list_item) => (
          <li key={list_item.id}>
            <DisplayItem data={list_item} liked={checkLiked(list_item)}/>
          </li>
        ))}
        end of items
      </ul>
    </div>
  );
}

export default PostList;
