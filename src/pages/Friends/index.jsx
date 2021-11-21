import jsCookies from "js-cookies";
import React, { useContext, useState } from "react";
import MiniProfile from "../../components/MiniProfile";
import authorService from "../../services/author";
import { UserContext } from "../../UserContext";
import "./styles.css"

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
      console.log(e)
    }
  };

  return (
    <div className="friendsContainer">
      { followers.length >= 1 && <> <h3>Friends</h3>
      {followers.map((follower) => (
        <MiniProfile author={follower} />
      ))} </> }
      <br/>
      <div className="followRequestContainer">
        <input placeholder="User ID" onChange={(event) => setForeignId(event.target.value)} />
        <button onClick={onSubmit}>SEND FOLLOW REQUEST</button>
      </div>
    </div>
  );
}

export default Friends;