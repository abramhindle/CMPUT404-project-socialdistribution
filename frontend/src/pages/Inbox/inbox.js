import NewPost from '../../components/Posts/new-post';
import PlainPost from '../../components/Posts/post-plain';
import Sidebar from '../../components/Sidebar/sidebar';
import './inbox.css';

function Inbox() {
  return (
    <div className='Page'>
      <Sidebar/>
      <div className='Inbox'>
        <p>
            This is now the inbox page
        </p>
        <PlainPost/>
        <NewPost/>
      </div>
    </div>
  );
}

export default Inbox;