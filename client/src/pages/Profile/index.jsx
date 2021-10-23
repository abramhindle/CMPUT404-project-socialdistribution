import jsCookies from 'js-cookies';
import React, { useContext, useState } from 'react';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import './styles.css';
const Profile = () => {
  const { user } = useContext(UserContext);
  const [displayName, setDisplayName] = useState(user.displayName);
  const [profileImage, setProfileImage] = useState(user.profileImage);
  const [githubLink, setGithubLink] = useState(user.github)
  const handleProfileChange = async (event) => {
    try {
      // get self object
      const response = await authorService.getAuthor(user.author.authorID);
      const author_data = response.data;
      console.log(author_data);
      author_data.displayName = displayName;
      author_data.profileImage = profileImage;

      console.log(author_data);

      console.log(
        await authorService.updateAuthor(
          jsCookies.getItem('csrftoken'),
          user.author.authorID,
          author_data
        )
      );

    } catch (e) {
      setDisplayName('');
      setProfileImage('');
    }
  };

  return (
    <div className='profileContainer'>
      <h2>My Profile</h2>
      <p>Display Name: {user.author.displayName}</p>
      <p>Profile Image Link: {user.author.profileImage}</p>
      <p>Github Link: {user.author.github}</p>

      <div className='updateProfileContainer'>
        <label>
          New Display Name:
          <input
            type='text'
            onChange={(e) => setDisplayName(e.target.value)}
            defaultValue={user.displayName}
          ></input>
        </label>
        <br />
        <label>
          New Profile Image Link:
          <input
            type='text'
            onChange={(e) => {
              setProfileImage(e.target.value);
            }}
            defaultValue={user.author.profileImage}
          ></input>
        </label>
        <br />
        <label>
          New Gitub Link:
          <input
            type='text'
            onChange={(e) => setGithubLink(e.target.value)}
            defaultValue={user.author.github}
          ></input>
        </label>
      </div>

      <button onClick={handleProfileChange}>submit</button>
    </div>
  );
};

export default Profile;
