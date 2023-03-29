import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import "./profile-edit.css";
import "../pages.css";

import Sidebar from "../../components/Sidebar/sidebar";
import { get_author, update_author } from "../../api/author_api";
import { signInUser } from "../../reducer/userSlice";

const ProfileEdit = () => {
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const [displayName, setDisplayName] = useState(user.displayName);
  const [github, setGithub] = useState(user.github);
  const [profileImage, setProfileImage] = useState(user.profileImage);

  const submitProfile = async (e) => {
    e.preventDefault();
    update_author(user.id, displayName, github, profileImage, successUpdate);
  };

  const successUpdate = (res) => {
    dispatch(signInUser(res));
  };

  return (
    <div className="Page">
      <div>
        <Sidebar />
      </div>
      <div className="myprofile sidebar-offset">
        <form className="Auth-form" onSubmit={submitProfile}>
          <div>
            <input
              type="text"
              value={displayName}
              required
              onChange={(e) => setDisplayName(e.target.value)}
            />
          </div>
          <div>
            <input
              type="url"
              value={github}
              onChange={(e) => setGithub(e.target.value)}
            />
          </div>
          <div>
            <input
              type="url"
              value={profileImage}
              required
              onChange={(e) => setProfileImage(e.target.value)}
            />
          </div>
          <button
            id="comment-submit"
            //   disabled={comment ? false : true}
            type="submit"
            onClick={submitProfile}
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfileEdit;
