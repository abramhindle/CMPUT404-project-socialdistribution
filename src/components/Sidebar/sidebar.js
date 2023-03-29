import "./sidebar.css";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { clearUser } from "../../reducer/userSlice";
import { Link } from "react-router-dom";
import EditButton from "../Buttons/edit_button";

function Sidebar() {
  //Get user & url info
  const user = useSelector((state) => state.user);
  const port = window.location.port ? `:${window.location.port}` : "";
  const authorUrl = `//${window.location.hostname}${port}/user/${(user.id ?? "")
    .split("/")
    .pop()}`; // allows linking to the author who wrote the post

  //Handle Navigations
  const navigate = useNavigate();
  //Navigate to Stream
  const goToStream = () =>{
      navigate("/");
  }; //Navigate to Main Inbox Feed
  const goToInbox = () =>{
      navigate("/inbox");
  };//Navigate to Add Friends page
  const goToAdd = () => {
      navigate("/friends/");
  };//Navigate to Requests page
  const goToRequests = () => {
      navigate("/friends/requests");
  }; //Navigate to Post creation page
  const goToNewPost = () => {
      navigate("/posts/new");
  }; //Navigate to Upload Image page
  const goToImageUpload = () => {
      navigate("/posts/image");
  }
  
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
    <div>
      <div className="Sidebar">
        {/* Profile Preview */}
        <div className="Profile" id="profile-tab">
          <img className="profile-pic" src={user.profileImage} alt="profile" />
          <Link to={authorUrl + "/edit"}>
            <EditButton />
          </Link>

          <p>
            <Link to={authorUrl}>{user.displayName}</Link>
          </p>
          <div className="stats">
            <p>
              <Link to={"/friends/true"}>Friends: {numFriends}</Link>
            </p>
            <p>
              <Link to={"/friends/followers"}>Followers: {numFollowers}</Link>
            </p>
            <p>
              <Link to={"/friends/followed"}>Followed: {numFollowed}</Link>
            </p>
          </div>
        </div>
        {/* Navigation Menu */}
        <menu>
            <li>
                <button className='Page' id="stream" onClick={goToStream}>Stream</button>
                {/* Inbox Options Submenu, only show if Inbox selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' id="inbox" onClick={goToInbox}>Inbox</button>
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
                </ul>
            </li>
            <li>
                <button className='Page' onClick={goToNewPost} id="new">New Post</button>
                {/* Post Options Submenu, only show if Post selected */}
                <ul className="Options-bar">
                    <li>
                        <button className='Options' onClick={goToImageUpload}>Upload Image</button>
                    </li>
                </ul>
            </li>
            <li>
            <button className='Page' onClick={signOut}>Sign Out</button>
            </li>
        </menu>
      </div>
      {/*<div className='Right Sidebar'>

    </div>*/}
    </div>
  );
}

export default Sidebar;
