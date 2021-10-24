import jsCookies from 'js-cookies';
import React, { useContext, useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import './styles.css';
const Profile = () => {
  const { user, setUser } = useContext(UserContext);
  const [displayName, setDisplayName] = useState(user.author.displayName);
  const [profileImage, setProfileImage] = useState(user.author.profileImage);
  const [github, setGithub] = useState(user.author.github);
  const history = useHistory();
  const handleProfileChange = async (event) => {
    try {
      // get self object
      const response = await authorService.getAuthor(user.author.authorID);
      const author_data = response.data;
      console.log(author_data);
      author_data.displayName = displayName;
      author_data.profileImage = profileImage;
      author_data.github = github;

      console.log(author_data);

      console.log(
        await authorService.updateAuthor(
          jsCookies.getItem('csrftoken'),
          user.author.authorID,
          author_data
        )
      );
      setDisplayName(displayName);
      setProfileImage(profileImage);
      setGithub(github);
      setUser({
        ...user, author: {
          ...user.author,
          displayName: displayName,
          profileImage: profileImage,
          github: github
        }});
      console.log(user)

    } catch (e) {
      alert('Error updating profile.');
      setDisplayName('');
      setProfileImage('');
      setGithub('');
    }
  };

  // redirect to home if not logged in
  useEffect(() => {
    if (user.author.authorID === null) {
      history.push('/');
    }
  });

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
            defaultValue={user.author.displayName}
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
            onChange={(e) => setGithub(e.target.value)}
            defaultValue={user.author.github}
          ></input>
        </label>
      </div>

      <button onClick={handleProfileChange}>submit</button>
    </div>
  );
};

export default Profile;
