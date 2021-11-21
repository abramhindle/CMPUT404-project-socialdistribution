import React from "react";

const MiniProfile = ({ author }) => {
  return (
    <div className="miniProfile">
      <img src={author.profileImage} width="30px" height="30px" alt="profilepic"/>
      <div>{author.displayName}</div>
    </div>
  )
}

export default MiniProfile;