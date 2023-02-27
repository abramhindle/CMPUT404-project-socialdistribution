import './sidebar.css';
import * as Nav from "../../navigation/navigate-to-page";
import { navigateInbox } from '../../navigation/navigate-to-page';
import { navigateRequests } from '../../navigation/navigate-to-page';
import { navigateNewPost } from '../../navigation/navigate-to-page';

function Sidebar() {
  return (
    <div className="Sidebar">
        {/* Profile Preview */}
        <div className='Profile'>
            <p>Profile <br/>Placeholder</p>
        </div>
        {/* Navigation Menu */}
        <menu>
            <li>
                <button className='Page' onClick={navigateInbox}>Inbox</button>
                {/* Inbox Options Submenu, only show if Inbox selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' onClick={navigateInbox}>Feed</button>
                    </li>
                    <li>
                        <button className='Options'>Likes</button>
                    </li>
                    <li>
                        <button className='Options'>For You</button>
                    </li>
                </ul>
            </li>
            <li>
                <button className='Page' onClick={navigateRequests}>Friends</button>
                {/* Requests Options Submenu, only show if Requests selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' onClick={navigateRequests}>Pending</button>
                    </li>
                    <li>
                        <button className='Options'>True Friends</button>
                    </li>
                    <li>
                        <button className='Options'>Followed</button>
                    </li>
                    <li>
                        <button className='Options'>Followers</button>
                    </li>
                </ul>
            </li>
            <li>
                <button className='Page' onClick={navigateNewPost}>Post</button>
                {/* Post Options Submenu, only show if Post selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' onClick={navigateNewPost}>New Post</button>
                    </li>
                    <li>
                        <button className='Options'>My Posts</button>
                    </li>
                </ul>

            </li>
        </menu>
    </div>
  );
}

export default Sidebar;