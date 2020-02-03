import React from "react";
import "../../styles/post/PostDropDown.scss";
import Dropdown from "react-bootstrap/Dropdown";
import editIcon from "../../images/edit-pencil.svg";
import deleteIcon from "../../images/del-bin.svg";
import linkIcon from "../../images/link.svg";

const PostDropDown = () => (
  <div>
    <Dropdown.Item>
      <img src={editIcon} alt="pencil-icon" />
      <span className="post-dropdown-text">Edit</span>
    </Dropdown.Item>
    <Dropdown.Divider />
    <Dropdown.Item>
      <img src={deleteIcon} alt="del-icon" />
      <span className="post-dropdown-text">Delete</span>
    </Dropdown.Item>
    <Dropdown.Divider />
    <Dropdown.Item>
      <img src={linkIcon} alt="link-icon" />
      <span className="post-dropdown-text">Copy link to post</span>
    </Dropdown.Item>
  </div>
);

export default PostDropDown;
