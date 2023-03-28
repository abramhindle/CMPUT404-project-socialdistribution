import { useState } from "react";
import { useSelector } from "react-redux";
import "./profile-edit.css";
import "../pages.css";

import Sidebar from "../../components/Sidebar/sidebar";

const ProfileEdit = () => {
  const user = useSelector((state) => state.user);
  const [displayName, setDisplayName] = useState(user.displayName);
  const [github, setGithub] = useState(user.github);
  const [profileImage, setProfileImage] = useState(user.profileImage);

  return (
    <div className="Page">
      <div>
        <Sidebar />
      </div>
      <div className="myprofile sidebar-offset">
        <input
          type="text"
          value={displayName}
          onChange={(e) => setDisplayName(e.value)}
        />
        <input type="url" value={github} onChange={(e) => setGithub(e.value)} />
        <input
          type="url"
          value={profileImage}
          onChange={(e) => setProfileImage(e.value)}
        />
        <button
          id="comment-submit"
          //   disabled={comment ? false : true}
          //   onClick={submitComment}
        >
          Submit
        </button>
      </div>
    </div>
  );
};

export default ProfileEdit;
