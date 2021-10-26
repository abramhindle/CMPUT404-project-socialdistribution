import React from "react";
import { Nav } from "react-bootstrap";
import Posts from "./Posts";
import { useDispatch, useSelector } from "react-redux";

// Content of home page; tabs to select which list of posts to view
function HomeContent() {
  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  return (
    <div className="m-2">
      <Nav fill variant="tabs" defaultActiveKey="1">
        <Nav.Item>
          <Nav.Link eventKey="1">All Posts</Nav.Link>
        </Nav.Item>
        <Nav.Item>
          {userInfo ? (
            <Nav.Link eventKey="2">Friend Posts</Nav.Link>
          ) : (
            <Nav.Link eventKey="2" disabled>
              Friend Posts
            </Nav.Link>
          )}
        </Nav.Item>
        <Nav.Item>
          {userInfo ? (
            <Nav.Link eventKey="3">My Posts</Nav.Link>
          ) : (
            <Nav.Link eventKey="3" disabled>
              My Posts
            </Nav.Link>
          )}
        </Nav.Item>
      </Nav>
      <Posts />
    </div>
  );
}
export default HomeContent;
