import React from "react";
import { useHistory } from "react-router";

const MiniProfile = ({ author }) => {
  const history = useHistory();

  const handleError = e => {
    e.target.onerror = null;
    e.target.src = '/static/assets/anonProfile.png';
  }

  const goToProfile = () => {
    history.push(`/author/${author.id.split("/").at(-1)}`)
  }

  return (
    <div className="miniProfile" onClick={goToProfile}>
      <img onError={handleError} src={author.profileImage || '/static/assets/anonProfile.png'} width="30px" height="30px" alt="profilepic"/>
      <div>{author.displayName}</div>
    </div>
  )
}

export default MiniProfile;