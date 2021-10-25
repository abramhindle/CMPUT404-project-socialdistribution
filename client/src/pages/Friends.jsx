import jsCookies from "js-cookies";
import React, { useContext, useState } from "react";
import authorService from "../services/author";
import { UserContext } from "../UserContext";

const Friends = ({ followers }) => {
  const [ foreignId, setForeignId ] = useState("");
  const { user } = useContext(UserContext);

  const onSubmit = async (event) => {
    try {
      const actorResponse = await authorService.getAuthor(user.author.authorID);
      const objectResponse = await authorService.getAuthor(foreignId)
      const response = await authorService.follow(jsCookies.getItem("csrftoken"), foreignId, actorResponse.data, objectResponse.data);

      console.log(response)
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
          <li key={follower.id}>{follower.displayName}</li>
        ))}
      </ul>
    </div>
  );
}

export default Friends;