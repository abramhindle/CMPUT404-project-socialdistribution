import React from "react";

const MiniProfile = ({ author }) => {

  const handleError = e => {
    e.target.onerror = null;
    e.target.src = 'static/assets/anonProfile.png';
  }

  return (
    <div className="miniProfile">
      <img src={author.profileImage || 'static/assets/anonProfile.png'} width="30px" height="30px" alt="profilepic"/>
      <div>{author.displayName}</div>
    </div>
  )
}

export default MiniProfile;