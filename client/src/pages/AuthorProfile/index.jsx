import jsCookies from 'js-cookies';
import React, { useContext, useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import './styles.css';
import { useParams } from 'react-router';

const AuthorProfile = () => {
  const { user, setUser } = useContext(UserContext);
  const [authorInfo, setAuthorInfo] = useState();
  const [pageAuthorFollowed, setPageAuthorFollowed] = useState(false);
  const [youAreFollowed, setYouAreFollowed] = useState(false);

  const pageAuthorID = useParams().id;

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await authorService.getAuthor(pageAuthorID);
        const author_data = response.data;
        setAuthorInfo(author_data);
      } catch (e) {
        alert('Error fetching author profile');
      }
    }

    async function fetchFollowStatus() {
      try {
        await authorService.checkIsFollowing(
          pageAuthorID,
          user.author.authorID
        );
        setPageAuthorFollowed(true);
      } catch (e) {
        setPageAuthorFollowed(false);
      }

      try {
        await authorService.checkIsFollowing(
          user.author.authorID,
          pageAuthorID
        );
        setYouAreFollowed(true);
      } catch (e) {
        setYouAreFollowed(false);
      }
    }

    fetchData();
    fetchFollowStatus();
  }, [pageAuthorID, user]);

  const AuthorPage = () => {
    return (
      <div className='profileContainer'>
        <h2>Author Profile</h2>
        <img
          src={authorInfo && authorInfo.profileImage}
          width='150'
          height='150'
          alt='profilepic'
        />
        <p>Display Name: {authorInfo && authorInfo.displayName}</p>
        <p>Profile Image Link: {authorInfo && authorInfo.profileImage}</p>
        <p>Github Link: {authorInfo && authorInfo.github}</p>
        <FollowStatus />
      </div>
    );
  };

  const FollowStatus = () => {
    console.log(pageAuthorFollowed);
    console.log(youAreFollowed);
    if (pageAuthorFollowed && youAreFollowed) {
      return <p>Wow! You guys are friends!</p>;
    } else if (pageAuthorFollowed) {
      return <p>You are following this author.</p>;
    } else if (youAreFollowed) {
      return <p>This author is following you.</p>;
    } else {
      return <p></p>;
    }
  };

  return (
    <div>
      {authorInfo === null ? (
        <h1>This author does not exist</h1>
      ) : (
        <AuthorPage />
      )}
    </div>
  );
};

export default AuthorProfile;
