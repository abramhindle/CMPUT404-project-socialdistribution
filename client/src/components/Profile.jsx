import React from "react";
import githubMark from "../resources/githubMark/githubMark120px.png"

const Profile = ({ author, buttonText, onClick }) => {
  console.log(author)
  return (
    <> { author &&
    <div>
      <div className="profileHeader">
        <img src={author.profileImage} width="200" height="200" alt="profilepic"/>
        <div className="profileHeaderInner">
          <h1>{author.displayName}</h1>
          <p>{author.authorID ? author.authorID : author.id.split("/").at(-1)}</p>
          { author.github && <a href={author.github}><img src={githubMark} width="25em" alt="github mark"/><div>{author.github}</div></a> }
          <div className="profileButton" onClick={onClick}>{buttonText}</div>
        </div>
      </div>
    </div>}
    </>
  )
};

export default Profile;