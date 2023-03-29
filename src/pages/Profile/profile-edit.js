import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import "./profile-edit.css";
import "../pages.css";

import Sidebar from "../../components/Sidebar/sidebar";
import { update_author } from "../../api/author_api";
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
        <h3 id="title">Update Profile</h3>

        <form className="profile-update-form" onSubmit={submitProfile}>
          <div>
            Display Name
            <input
              type="text"
              value={displayName}
              placeholder="Display Name"
              required
              onChange={(e) => setDisplayName(e.target.value)}
            />
          </div>
          <div>
            Profile Image
            <input
              type="url"
              value={profileImage}
              placeholder="Profile Image (Optional)"
              onChange={(e) => setProfileImage(e.target.value)}
            />
          </div>
          <div>
            Github
            <input
              type="url"
              value={github}
              placeholder="Github (Optional)"
              onChange={(e) => setGithub(e.target.value)}
            />
          </div>
          <button
            id="comment-submit"
            //   disabled={comment ? false : true}
            type="submit"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
};

export default ProfileEdit;
