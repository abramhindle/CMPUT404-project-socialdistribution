import './styles.css';
import jsCookies from 'js-cookies';
import { Parser, HtmlRenderer } from 'commonmark';
import { useContext, useState } from 'react';
import authorService from '../../services/author';
import postService from '../../services/post';
import { UserContext } from '../../UserContext';
import { v4 as uuidv4 } from 'uuid';

const SubmitPost = () => {
  const { user } = useContext(UserContext);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [contentType, setContentType] = useState('text/plain');
  const [content, setContent] = useState('');
  const [categories, setCategories] = useState('');
  const [visibility, setVisibility] = useState('PUBLIC');
  const [unlisted, setUnlisted] = useState(false);
  const CMParser = new Parser();
  const CMWriter = new HtmlRenderer();



  const parseCategories = (categories) => {
    if (categories.trim().length === 0) {
      return [];
    }
    return categories.split(',').map((item) => item.trim());
  };

  const parseVisibility = (friendsOnly) => {
    if (friendsOnly) return 'FRIENDS';
    return 'PUBLIC';
  };

  const isEmptyString = (str) => {
    return str.length === 0 || str.trim().length === 0 ? true : false;
  }

  const submitPost = async () => {
    if (isEmptyString(title)) {
      alert("Title cannot be empty.");
      return
    }
    if (isEmptyString(description)) {
      alert('Description cannot be empty.');
      return;
    }
    if (isEmptyString(contentType)) {
      alert('Please choose a content type.');
      return;
    }
    if (isEmptyString(content)) {
      alert('Post content cannot be empty');
      return;
    }
    try {
      const response = await authorService.getAuthor(user.author.authorID);
      const author_data = response.data;
      console.log(author_data);
      const date = new Date();

      let postData = {
        type: "post",
        title: title,
        id: null,
        source: null,
        origin: null,
        description: description,
        contentType: contentType,
        content: content,
        author: author_data,
        categories: parseCategories(categories),
        count: 0,
        comments: null,
        published: date.toISOString(),
        visibility: visibility,
        unlisted: unlisted
      }
      console.log(postData);

      const postresponse = await postService.createPost(
        jsCookies.getItem('csrftoken'),
        user.author.authorID,
        postData
      );



    } catch (e) {
      console.log(e);
      alert("Error submitting post")
    }




    console.log(title);
    console.log(description);
    console.log(contentType);
    console.log(content);
    console.log(categories);
    console.log(visibility);
    console.log(unlisted);
  };

  return (
    <div className='submitPostContainer'>
      <h2>Post Submission</h2>
      <div className='horizontalDiv'>
        <p>Title: </p>
        <input onChange={(e) => setTitle(e.target.value)}></input>
      </div>
      <div className='horizontalDiv'>
        <p>Description: </p>
        <input onChange={(e) => setDescription(e.target.value)}></input>
      </div>
      <select
        className='selectContentType'
        name='Content Type'
        value={contentType}
        onChange={(e) => setContentType(e.target.value)}
      >
        <option>text/plain</option>
        <option>text/markdown</option>
      </select>

      <div className='textContentInput'>
        <p>Content: </p>
        <textarea onChange={(e) => setContent(e.target.value)}></textarea>
      </div>
      {contentType === 'text/markdown' ? (
        <div>
          <p className='previewTitle'>Preview</p>
          <div
            className='cmPreview'
            dangerouslySetInnerHTML={{
              __html: CMWriter.render(CMParser.parse(content)),
            }}
          ></div>
        </div>
      ) : (
        <></>
      )}
      <div className='horizontalDiv'>
        <p>Categories:</p>
        <input
          onChange={(e) => setCategories(parseCategories(e.target.value))}
        ></input>
      </div>

      <input
        type='checkbox'
        onChange={(e) => setVisibility(parseVisibility(e.target.value))}
      ></input>
      <label>Friends-Only</label>
      <br />
      <div className="horizontalDiv">

      </div>
      <input
        type='checkbox'
        onChange={(e) => {
          if (e.target.value !== false) {
            setUnlisted(true);
          } setUnlisted(e.target.value);
        }}
      ></input>
      <label>Unlisted</label>
      <br />
      <button onClick={submitPost}>Submit</button>
    </div>
  );
};

export default SubmitPost;
