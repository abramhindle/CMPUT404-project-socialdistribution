import './styles.css';
import jsCookies from 'js-cookies';
import { Parser, HtmlRenderer } from 'commonmark';
import { useHistory } from 'react-router';
import { useContext, useState } from 'react';
import authorService from '../../services/author';
import postService from '../../services/post';
import { UserContext } from '../../UserContext';
import { v4 as uuidv4 } from 'uuid';

const SubmitPost = () => {
  const { user } = useContext(UserContext);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [postType, setPostType] = useState('Text');
  const [contentType, setContentType] = useState('text/plain');
  const [content, setContent] = useState('');
  const [categories, setCategories] = useState([]);
  const [visibility, setVisibility] = useState('PUBLIC');
  const [unlisted, setUnlisted] = useState(false);
  const CMParser = new Parser();
  const CMWriter = new HtmlRenderer();
  const history = useHistory();

  const parseCategories = (categoriesString) => {
    if (categoriesString.trim().length === 0) {
      return [];
    }
    return categoriesString.split(',').map((item) => item.trim());
  };

  const parseVisibility = (friendsOnly) => {
    if (friendsOnly) return 'FRIENDS';
    return 'PUBLIC';
  };

  const isEmptyString = (str) => {
    return str.length === 0 || str.trim().length === 0 ? true : false;
  };

  const submitPost = async () => {
    if (isEmptyString(title)) {
      alert('Title cannot be empty.');
      return;
    }
    if (isEmptyString(description)) {
      alert('Description cannot be empty.');
      return;
    }
    if (isEmptyString(postType)) {
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
        type: 'post',
        title: title,
        id: null,
        source: null,
        origin: null,
        description: description,
        contentType: contentType,
        content: content,
        author: author_data,
        categories: categories,
        count: 0,
        comments: null,
        published: date.toISOString(),
        visibility: visibility,
        unlisted: unlisted,
      };
      const submitResponse = await postService.createPost(
        jsCookies.getItem('csrftoken'),
        user.author.authorID,
        postData
      );
      console.log(submitResponse?.data)
      history.go(0);
    } catch (e) {
      console.log(e);
      alert('Error submitting post');
    }
  };

  const handleFile = (file) => {
    const fileReader = new FileReader();
    fileReader.addEventListener('load', (event) => {
      let dataType = event.target.result.split(',')[0].split(':')[1];
      if (dataType !== 'image/png;base64' && dataType !== 'image/jpeg;base64') {
        dataType = 'application/base64';
      }
      console.log(event.target.result);
      setContent(event.target.result);
      setContentType(dataType);
    });

    if (file) {
      fileReader.readAsDataURL(file);
    } else {
      setContent('');
    }
  };

  const renderContentInput = (type) => {
    if (type === 'Text') {
      return (
        <div className='textContentInput'>
          <p>Content: </p>
          <textarea
            onChange={(e) => {
              setContent(e.target.value);
              setContentType('text/plain');
            }}
          ></textarea>
        </div>
      );
    } else if (type === 'Markdown') {
      return (
        <div>
          <div className='textContentInput'>
            <p>Content: </p>
            <textarea
              onChange={(e) => {
                setContent(e.target.value);
                setContentType('text/markdown');
              }}
            ></textarea>
          </div>
          <div>
            <p className='previewTitle'>Preview</p>
            <div
              className='cmPreview'
              dangerouslySetInnerHTML={{
                __html: CMWriter.render(CMParser.parse(content)),
              }}
            ></div>
          </div>
        </div>
      );
    } else if (type === 'File') {
      return (
        <div>
          <br />
          <input
            type='file'
            onChange={(e) => {
              handleFile(e.target.files[0]);
            }}
          ></input>
          <br />
          <br />
          {contentType.includes('image') ? <img className="previewPic" alt='content_img' src={content} /> : <></>}
        </div>
      );
    }
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
      <select onChange={(e) => setPostType(e.target.value)}>
        <option>Text</option>
        <option>Markdown</option>
        <option>File</option>
      </select>
      <div>{renderContentInput(postType)}</div>
      <div className='horizontalDiv'>
        <p>Categories:</p>
        <input
          onChange={(e) => setCategories(parseCategories(e.target.value))}
        ></input>
      </div>

      <input
        type='checkbox'
        onChange={(e) => setVisibility(parseVisibility(e.target.checked))}
      ></input>
      <label>Friends-Only</label>
      <br />
      <div className='horizontalDiv'></div>
      <input
        type='checkbox'
        value={postType}
        onChange={(e) => {
          setUnlisted(e.target.checked);
        }}
      ></input>
      <label>Unlisted</label>
      <br />
      <button onClick={submitPost}>Submit</button>
    </div>
  );
};

export default SubmitPost;
