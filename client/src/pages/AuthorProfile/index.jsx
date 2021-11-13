import React, { useContext, useEffect, useState } from 'react';
import authorService from '../../services/author';
import { UserContext } from '../../UserContext';
import './styles.css';
import { useParams } from 'react-router';
import Profile from '../../components/Profile';
import jsCookies from 'js-cookies';

const AuthorProfile = () => {
  const { user } = useContext(UserContext);
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


  const follow = async (event) => {
    try {
      const actorResponse = await authorService.getAuthor(user.author.authorID);
      const objectResponse = await authorService.getAuthor(authorInfo.id.split("/").at(-1))
      const response = await authorService.follow(jsCookies.getItem("csrftoken"), authorInfo.id.split("/").at(-1), actorResponse.data, objectResponse.data);

      console.log(response)
    } catch (e) {
      console.log(e)
    }
  };


  const AuthorPage = () => {
    return (
      <div className='profileContainer'>
        <>{ pageAuthorFollowed ? 
            <Profile author={authorInfo} buttonText={FollowStatus()} />  
            :
            <Profile author={authorInfo} buttonText="Follow" onClick={follow} />
          }
        </>
      </div>
    );
  };

  const FollowStatus = () => {
    console.log(pageAuthorFollowed);
    console.log(youAreFollowed);
    if (pageAuthorFollowed && youAreFollowed) {
      return "Wow! You guys are friends!";
    } else if (pageAuthorFollowed) {
      return "You are following this author";
    } else if (youAreFollowed) {
      return "This author is following you";
    } else {
      return "";
    }
  };

  return (
    <div>
      {AuthorPage()}
    </div>
  );
};

export default AuthorProfile;
