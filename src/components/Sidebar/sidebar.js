import './sidebar.css';
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { clearUser } from "../../reducer/userSlice";

function Sidebar() {
    //Get user & url info
    const user = useSelector((state) => state.user);
    const port = window.location.port ? `:${window.location.port}` : "";
    const authorUrl = `//${window.location.hostname}${port}/user/${(user.id ?? "").split('/').pop()}`; // allows linking to the author who wrote the post
    const followUrl = `//${window.location.hostname}${port}/user/${(user.id ?? "").split('/').pop()}?tab=followers`
   
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
    //Signout functionality
    const dispatch = useDispatch();
    const signOut = () => {
      dispatch(clearUser(user));
    };

    //Get stats
    //TODO: Attach to backend to pull actual numbers
    var numFollowed = 1000;
    var numFollowers = 99;
    var numFriends = 27;

  return (
    <nav className="Sidebar">
        {/* Profile Preview */}
        <div className='Profile' id="profile-tab">
            <img className="profile-pic" src={user.profileImage} alt="profile" href={authorUrl}/>
            <p><a href={authorUrl}>{user.displayName}</a></p>
            <div className="stats">
                <p><a href={followUrl}>Friends: {numFriends}</a></p>
                <p><a href={followUrl}>Followers: {numFollowers}</a></p>
                <p><a href={followUrl}>Followed: {numFollowed}</a></p>
            </div>
            
        </div>
        {/* Navigation Menu */}
        <menu>
            <li>
                <button className='Page' id="stream" onClick={goToInbox}>Stream</button>
                {/* Inbox Options Submenu, only show if Inbox selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' id="inbox">Inbox</button>
                    </li>
                    <li>
                        <button className='Options'>Likes</button>
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
                <button className='Page' onClick={goToNewPost} id="new">New Post</button>
                {/* Post Options Submenu, only show if Post selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options'>My Posts</button>
                    </li>
                </ul>
            </li>
            <li>
            <button className='Page' onClick={signOut}>Sign Out</button>
            </li>
        </menu>
    </nav>
  );
}

export default Sidebar;