import './styles.css';
import jsCookies from 'js-cookies';
import { useHistory } from 'react-router';
import { useContext } from 'react';
import authorService from '../../services/author';
import postService from '../../services/post';
import { UserContext } from '../../UserContext';
import PostEdit from '../../components/PostEdit';

const SubmitPost = () => {
  const { user } = useContext(UserContext);
  const history = useHistory();

  const submitPost = async (postData) => {
      try {
      const response = await authorService.getAuthor(user.author.authorID);
      console.log(response.data)
      postData.author = response.data;
      console.log(postData)
      const submitResponse = await postService.createPost(
        jsCookies.getItem('csrftoken'),
        user.author.authorID,
        postData
      );
      console.log(submitResponse)
      history.push(`/author/${user.author.authorID}/post/${submitResponse.data.id.split("/").at(-1)}`);
    } catch (e) {
      console.log(e);
      alert('Error submitting post');
    }
  };

  return (
    <div className='submitPostContainer'>
      <PostEdit onSubmit={submitPost} post={{}} />
    </div>
  );
};

export default SubmitPost;
