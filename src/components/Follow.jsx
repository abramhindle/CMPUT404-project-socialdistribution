import jsCookies from "js-cookies";
import React, { useContext } from "react";
import authorService from "../services/author";
import { UserContext } from "../UserContext";
import MiniProfile from "./MiniProfile";

const Follow = ({ follow, followers }) => {
  const { user } = useContext(UserContext);

  const acceptFollow = async () => {
    console.log(follow)
    const response = await authorService.acceptFollow(jsCookies.getItem("csrftoken"), user.author.authorID, follow.actor.id.split("/").at(-1));
    console.log(response);
  };

  return (
    <div>
      { followers.find(f => f.id === follow.actor.id ) ? <></> :
          <div className="itemContainer" style={{cursor: "pointer"}} onClick={acceptFollow}>
            <MiniProfile author={follow.actor} /> <div className="followText">wants to follow you! Click to accept.</div>
          </div>
      }
    </div>
  );
};

export default Follow;