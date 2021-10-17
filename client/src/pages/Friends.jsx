import jsCookies from "js-cookies";
import React, { useContext, useState } from "react";
import followService from "../services/follow";
import { UserContext } from "../UserContext";

const Friends = ({ followers }) => {
  const [ foreignId, setForeignId ] = useState("");
  const { user } = useContext(UserContext);

  const onSubmit = async (event) => {
    try {
      const response = await followService.follow(user, foreignId, jsCookies.getItem("csrftoken"));
    } catch (e) {
      console.log("error wee woo")
    }
  };

  return (
    <div>
      <input onChange={(event) => setForeignId(event.target.value)} />
      <button onClick={onSubmit} />
      <ul>
        {followers.map((follower) => (
          <li key={follower}>{follower}</li>
        ))}
      </ul>
    </div>
  );
}

export default Friends;