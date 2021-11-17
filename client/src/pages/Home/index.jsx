import Like from "../../components/Like";
import Follow from "../../components/Follow";
import { UserContext } from "../../UserContext";
import { useEffect, useState } from 'react';
import { useContext } from "react";
import authorService from "../../services/author";
import jsCookies from "js-cookies";
import './styles.css'
import PostPreview from "../../components/PostPreview";
import postService from '../../services/post';

const Home = ({ inbox, setInbox, followers }) => {
  const { user } = useContext(UserContext);

  const [publicPostList, setPublicMyPostList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const fetchMyPost = async () => {
      try {
        const response = await postService.getPostFeed(
          jsCookies.getItem('csrftoken'),
          currentPage,
          5
        );
        const postData = response.data?.items;
        console.log(postData);
        setPublicMyPostList(postData||[]);
      } catch (e) {
        console.log(e);
      }
    };
    fetchMyPost();
  }, [user, currentPage]);

  const generateListView = (postList) => {
    if (postList == null || postList === []) {
      return <p>Hi</p>;
    }

    return postList.map((item, i) => {
      return <PostPreview key={item.id} post={item} />;
    });
  };

  const clearInbox = async () => {
    try {
      const response = await authorService.clearInbox(jsCookies.getItem("csrftoken"), user.author.authorID);
      console.log(response)
      setInbox([])
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div>
      <br></br>
      <div className='mainContainer'>
        {inbox &&
          inbox.map((item) => {
            console.log(item);
            if (item.type.toLowerCase() === 'post') {
              return <PostPreview key={item.id} post={item} />;
            } else if (item.type.toLowerCase() === 'follow') {
              return (
                <Follow
                  key={`${item.actor.id};${item.object.id}`}
                  follow={item}
                  followers={followers}
                />
              );
            } else if (item.type.toLowerCase() === 'like') {
              return (
                <Like key={`${item.object};${item.author.id}`} like={item} />
              );
            } else {
              return <></>;
            }
          })}
        <button onClick={clearInbox}>Clear Inbox</button>
      </div>
      <div className='myPostContainer'>
        <h3>My Feed</h3>
        {generateListView(publicPostList)}
      </div>
      <div className='paginationContainer'>
        {currentPage !== 1 ? (
          <p onClick={() => setCurrentPage(currentPage - 1)}>Previous Page</p>
        ) : (
          <></>
        )}
        {publicPostList.length < 5 ? (
          <></>
        ) : (
          <p
            id='myPostNextPage'
            onClick={() => setCurrentPage(currentPage + 1)}
          >
            Next Page
          </p>
        )}
      </div>
    </div>
  );
}

export default Home;