import React from "react";
import { useHistory } from "react-router";
import githubMark from "../resources/githubMark/githubMark120px.png"

const Profile = ({ author, buttonText, onClick }) => {
  const history = useHistory();
  const sendPost = () => {
    history.push(`/submit/${author.id.split("/").at(-1)}`)
  }

  return (
    <> { author &&
    <div>
      <div className="profileHeader">
        <img src={author.profileImage || '/static/assets/anonProfile.png'} width="200" height="200" alt="profilepic"/>
        <div className="profileHeaderInner">
          <h1>{author.displayName}</h1>
          <p>{author.authorID ? author.authorID : author.id.split("/").at(-1)}</p>
          { author.github && <a href={author.github}><img src={githubMark} width="25em" alt="github mark"/><div>{author.github}</div></a> }
          <div style={{display:"flex", flexDirection: "row"}}>
            <div className="profileButton" onClick={onClick}>{buttonText}</div>
            <div className="profileButton" onClick={sendPost} style={{marginLeft: "5px"}}>Send Post</div>
          </div>
        </div>
      </div>
    </div>}
    </>
  )
};

export default Profile;