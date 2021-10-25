import { useContext, useEffect, useState } from 'react';
import { useHistory } from 'react-router';
import jsCookies from 'js-cookies';
import './styles.css';
import { UserContext } from '../../UserContext';
import postService from '../../services/post';
const MyPosts = () => {
  const { user } = useContext(UserContext);
  const [myPostList, setMyPostList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const history = useHistory();

  useEffect(() => {
    const fetchMyPost = async () => {
      try {
        const response = await postService.getPosts(
          jsCookies.getItem('csrftoken'),
          user.author.authorID,
          currentPage
        );
        const postData = response.data?.items;
        console.log(postData);
        setMyPostList(postData);
      } catch (e) {
        console.log(e);
      }
    };
    fetchMyPost();
  }, [user, currentPage]);

  const goToPost = (postID, authorID) => {
    postID = postID.split('/').at(-1);
    authorID = authorID.split('/').at(-1);

    history.push(`/author/${authorID}/post/${postID}`);
  };

  const generateListView = (postList) => {
    if (postList == null) {
      return <p>Hi</p>;
    }

    return postList.map((item, i) => {
      return (
        <div
          className='postPreviewContainer'
          onClick={() => {
            goToPost(item.id, item.author.id);
          }}
        >
          <p>Title: {item.title}</p>
          <p>Description: {item.description}</p>
          <p>Author: {item.author.displayName}</p>
        </div>
      );
    });
  };

  return (
    <div>
      <div className='myPostContainer'>
        <h3>My Posts</h3>
        {generateListView(myPostList)}
      </div>
      <div className='paginationContainer'>
        {currentPage !== 1 ? (
          <p onClick={() => setCurrentPage(currentPage - 1)}>Previous Page</p>
        ) : (
          <></>
        )}
        {myPostList.length < 5 ? (
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
};

export default MyPosts;
