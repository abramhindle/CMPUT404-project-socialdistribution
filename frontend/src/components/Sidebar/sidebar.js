import './sidebar.css';
import { useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";


function Sidebar() {
    //Get user info
    const user = useSelector((state) => state.user);

    const port = window.location.port ? `:${window.location.port}` : "";
    const authorUrl = `//${window.location.hostname}${port}/user/${(user.id ?? "").split('/').pop()}`; // allows linking to the author who wrote the post

    //Handle Navigations
    const navigate = useNavigate();
    //Navigate to Main Inbox Feed
    const goToInbox = () =>{
        navigate("/");
    };//Navigate to Requests page
    const goToAdd = () => {
        navigate("/friends/");
    };//Navigate to Requests page
    const goToRequests = () => {
        navigate("/friends/requests");
    };//Navigate to Requests page
    const goToTrue = () => {
        navigate("/friends/true");
    };//Navigate to Followed page
    const goToFollowed = () => {
        navigate("/friends/followed");
    };//Navigate to Followers page
    const goToFollowers = () => {
        navigate("/friends/followers");     
    };//Navigate to Post creation page
    const goToNewPost = () => {
        navigate("/posts/new");
    };

  return (
    <nav className="Sidebar">
        {/* Profile Preview */}
        <div className='Profile'>
            <img className="profile-pic" src={user.profileImage} alt="profile"/>
            <p><a href={authorUrl}>{user.displayName}</a></p>
            <div className="stats">
                <p>Friends: 0</p>
                <p>Followers: 0</p>
                <p>Followed: 0</p>
            </div>
            
        </div>
        {/* Navigation Menu */}
        <menu>
            <li>
                <button className='Page' id="inbox-page-nav" onClick={goToInbox}>Inbox</button>
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
                <button className='Page' onClick={goToAdd}>Friends</button>
                {/* Requests Options Submenu, only show if Friends selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' onClick={goToRequests}>Pending</button>
                    </li>
                    <li>
                        <button className='Options' onClick={goToTrue}>True Friends</button>
                    </li>
                    <li>
                        <button className='Options' onClick={goToFollowed}>Followed</button>
                    </li>
                    <li>
                        <button className='Options' onClick={goToFollowers}>Followers</button>
                    </li>
                </ul>
            </li>
            <li>
                <button className='Page' onClick={goToNewPost}>Post</button>
                {/* Post Options Submenu, only show if Post selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' onClick={goToNewPost}>New Post</button>
                    </li>
                    <li>
                        <button className='Options'>My Posts</button>
                    </li>
                </ul>

            </li>
        </menu>
    </nav>
  );
}

export default Sidebar;