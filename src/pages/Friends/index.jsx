import jsCookies from "js-cookies";
import React, { useContext, useState } from "react";
import MiniProfile from "../../components/MiniProfile";
import authorService from "../../services/author";
import { UserContext } from "../../UserContext";
import "./styles.css"

const Friends = ({ followers, setFollowers }) => {
  const [ foreignId, setForeignId ] = useState("");
  const { user } = useContext(UserContext);

  const onSubmit = async (event) => {
    try {
      const actorResponse = await authorService.getAuthor(user.author.authorID);
      const objectResponse = await authorService.getAuthor(foreignId)
      await authorService.follow(jsCookies.getItem("csrftoken"), foreignId, actorResponse.data, objectResponse.data);

    } catch (e) {
      console.log(e)
    }
  };

  const removeFriend = async (follower) => {
    const authorResponse = await authorService.getAuthor(user.author.authorID);
    authorService.removeFollower(jsCookies.getItem("csrftoken"), authorResponse.data.id.split("/").at(-1), follower.id.split("/").at(-1))
    setFollowers(followers.filter((foll) => {
      return foll.id !== follower.id
    }))
  }

  return (
    <div className="friendsContainer">
      { followers.length >= 1 && <> <h3>Friends</h3>
      {followers.map((follower) => (
        <div style={{display: "flex", flexDirection: "row"}}><MiniProfile author={follower} /> <div onClick={() => { removeFriend(follower)}} className="postButton" style={{margin: "15px"}}>Remove Friend</div></div>
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