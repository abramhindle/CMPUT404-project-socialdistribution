import React, { useState, useEffect } from "react";
import { Nav } from "react-bootstrap";
import Posts from "./Posts";
import { useDispatch, useSelector } from "react-redux";
import Message from "../components/Message";
import { getPosts } from "../actions/postActions";

// Content of home page; tabs to select which list of posts to view
function HomeContent() {
  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const postList = useSelector((state) => state.postList);
  const { error, success, post } = postList;

  useEffect(() => {
    if (post == null) {
      dispatch(getPosts());
    }
  }, [dispatch, post]);

  const [message, setMessage] = useState("");
  const posts = post ? post.items : [];

  return (
    <div className="m-2">
      {message && <Message variant="danger">{message}</Message>}
      {error && <Message variant="danger">{error}</Message>}
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
      {posts.map((p) => (
        <Posts post={p} />
      ))}
    </div>
  );
}
export default HomeContent;
