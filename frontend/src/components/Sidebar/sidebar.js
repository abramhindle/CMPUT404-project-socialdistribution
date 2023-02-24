import './sidebar.css';

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
                <button className='Page'>Inbox</button>
                {/* Inbox Options Submenu, only show if Inbox selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options'>Feed</button>
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
                <button className='Page'>Requests</button>
                {/* Requests Options Submenu, only show if Requests selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options'>Your Requests</button>
                    </li>
                    <li>
                        <button className='Options'>Accounts You Follow</button>
                    </li>
                    <li>
                        <button className='Options'>Followers</button>
                    </li>
                </ul>
            </li>
            <li>
                <button className='Page'>Post</button>
                {/* Post Options Submenu, only show if Post selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options'>New Post</button>
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