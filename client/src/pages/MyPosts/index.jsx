import { useContext, useEffect, useState } from 'react';
import jsCookies from 'js-cookies';
import './styles.css';
import { UserContext } from '../../UserContext';
import PostPreview from '../../components/PostPreview';
import postService from '../../services/post';
const MyPosts = () => {
  const { user } = useContext(UserContext);
  const [myPostList, setMyPostList] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

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

  const generateListView = (postList) => {
    if (postList == null) {
      return <p>Hi</p>;
    }

    return postList.map((item, i) => {
      return (
        <PostPreview post={item} />
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
