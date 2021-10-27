import React from "react";

const Profile = ({ author }) => {
  console.log(author)
  return (
    <> { author &&
    <div>
      <img src={author.profileImage} width="150" height="150" alt="profilepic"/>
      <p>Display Name: {author.displayName}</p>
      <p>Profile Image Link: {author.profileImage}</p>
      <p>Github Link: {author.github}</p>
      <p>ID: {author.authorID ? author.authorID : author.id.split("/").at(-1)}</p>
    </div>}
    </>
  )
};

export default Profile;