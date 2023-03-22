import Comment from "./comment";
import PlainPost from "./post-text";
import React, { useEffect, useState } from "react";
import { get_liked } from "../../api/like_api";
import { useSelector } from "react-redux";

//TODO : like / follow request objects

export default function DisplayItem(props) {
    const user = useSelector((state) => state.user);
    const [liked, setLiked] = useState([]);
    const data = props.data;


    /*useEffect(() => {
      get_liked(user.id, setLiked);
    }, []);*/

    console.log(data);
  
    function checkLiked(item) {
      for (var i = 0; i < liked.length; i++) {
        if (liked[i].object === item.id) {
          return true;
        }
      }
      return false;
    }

    if (data.type === "comment"){
        //display comment
        return (<Comment data={data}/>);
    }
    else if (data.type === "post"){
        //display post
        return (<PlainPost post={data} liked={checkLiked(data)}/>);
    }
    else if (data.type === "like"){
        //display like object
    }
    else if (data.type === "follow"){
        //display follow request object
    }
    else{
        return;
    }
}