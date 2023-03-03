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
      </div>
    </div>
  );
}

export default Inbox;