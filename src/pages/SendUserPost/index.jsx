import jsCookies from 'js-cookies';
import { useHistory, useParams } from 'react-router';
import authorService from '../../services/author';
import postService from '../../services/post';
import PostEdit from '../../components/PostEdit';
import { UserContext } from '../../UserContext';
import { useContext, useEffect } from 'react';
import { useState } from 'react';

const SendUserPost = () => {
  const { foreignId } = useParams();
  const history = useHistory();
  const [ foreignUser, setForeignUser ] = useState({});
  const { user } = useContext(UserContext);

  useEffect(() => {
    authorService.getAuthor(foreignId)
        .then(res => setForeignUser(res.data)) 
        .catch(e => alert(e))
  }, [foreignId])

  const submitPost = async (postData) => {
    try {
      const response = await authorService.getAuthor(user.author.authorID);
      postData.author = response.data;
      await postService.sendPost(
        jsCookies.getItem('csrftoken'),
        foreignUser.id.split("/").at(-1),
        postData
      );
      history.push(`/author/${foreignUser.id.split("/").at(-1)}`);
    } catch (e) {
      console.log(e);
      alert('Error submitting post');
    }
  };

  return (
    <div className='submitPostContainer'>
      <h3>{ foreignUser?.displayName ? `Send Post to ${foreignUser?.displayName}`: "" }</h3>
      <PostEdit onSubmit={submitPost} post={{}} hideCheckboxes={true} />
      <br/>
      <br/>
    </div>
  );
};

export default SendUserPost;
