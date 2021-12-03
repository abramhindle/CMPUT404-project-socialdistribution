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
import InboxComment from "../../components/InboxComment";

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
      await authorService.clearInbox(jsCookies.getItem("csrftoken"), user.author.authorID);
      setInbox([])
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div>
      <br></br>
      <div className='mainContainer'>
        <h3>Inbox</h3>
        {inbox?.length !== 0 ? <> {
          inbox.map((item) => {
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
            } else if (item.type.toLowerCase() === 'comment') {
              return (
                <InboxComment key={`${item.object};${item.author.id}`} comment={item} />
              )
            } else if (item.type.toLowerCase() === 'post') {
              return (
                <PostPreview key={`${item.object};${item.author.id}`} post={item} />
              )
            } else {
              return <></>;
            }
          })}
            <button className="clearButton" onClick={clearInbox}>CLEAR INBOX</button>
          </>
          : <><p>Your inbox is empty.</p></>}
      </div>
      <div className='myPostContainer'>
        <h3>Public Posts</h3>
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
      <br/>
      <br/>
    </div>
  );
}

export default Home;