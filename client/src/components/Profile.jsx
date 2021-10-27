import React from "react";

const Profile = ({ author }) => {
  return (
    <div>
      <img src={author.profileImage} width="150" height="150" alt="profilepic"/>
      <p>Display Name: {author.displayName}</p>
      <p>Profile Image Link: {author.profileImage}</p>
      <p>Github Link: {author.github}</p>
    </div>
  )
};

export default Profile;