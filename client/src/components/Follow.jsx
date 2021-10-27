import jsCookies from "js-cookies";
import React, { useContext } from "react";
import authorService from "../services/author";
import { UserContext } from "../UserContext";

const Follow = ({ follow }) => {
  const { user } = useContext(UserContext);

  const acceptFollow = async () => {
    console.log(follow)
    const response = await authorService.acceptFollow(jsCookies.getItem("csrftoken"), user.author.authorID, follow.actor.id.split("/").at(-1));
    console.log(response);
  };

  return (
    <div className="itemContainer">  
      <p onClick={acceptFollow}>{ follow.actor.displayName } wants to follow you!</p>
    </div>
  );
};

export default Follow;