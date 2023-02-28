import NewPost from '../../components/Posts/new-post';
import PlainPost from '../../components/Posts/post-plain';
import Sidebar from '../../components/Sidebar/sidebar';
import './inbox.css';

function Inbox() {
  let pseudoPost = 
    {
      "title": "This is my post!",
      "author": "0c1d8f09-2395-4a9d-8fe3-de4bad85e468",
      "description": "this is a description",
      "contentType": "text/markdown",
      "content": "this is the content body",
      "visibility": "PUBLIC",
      "published" : "2023-02-28 05:45:42",
      "unlisted": false,
      "categories": ["web", "design"]
    }

  return (
    <div className='Page'>
      <Sidebar/>
      <div className='Inbox'>
        <p>
            This is now the inbox page
        </p>
        <PlainPost post={pseudoPost}/>
        <NewPost/>
      </div>
    </div>
  );
}

export default Inbox;