import jsCookies from "js-cookies";
import React, { useContext } from "react";
import authorService from "../services/author";
import { UserContext } from "../UserContext";

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
        <div className="itemContainer" onClick={acceptFollow}>{ follow.actor.displayName } wants to follow you!</div>
      }
    </div>
  );
};

export default Follow;