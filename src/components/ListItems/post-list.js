import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import PlainPost from "../../components/Posts/post-text";
import "./post-list.css";
import { get_liked } from "../../api/like_api";

function PostList({ user_list }) {
  const user = useSelector((state) => state.user);

  //gets a json object, and returns a list item for it

  const [liked, setLiked] = useState(null);

  useEffect(() => {
    get_liked(user.id, setLiked);
  }, []);

  function checkLiked(item) {
    for (var i = 0; i < liked.length; i++) {
      if (liked[i].object === item.id) {
        return true;
      }
    }
    return false;
  }

  return (
    liked && (
      <div className="posts">
        <ul className="postsList">
          {console.log(user_list)}
          {user_list.items.map((list_item) => (
            <li className="post" key={list_item.id}>
              <PlainPost post={list_item} liked={checkLiked(list_item)} />
            </li>
          ))}
          ;
        </ul>
      </div>
    )
  );
}

export default PostList;
