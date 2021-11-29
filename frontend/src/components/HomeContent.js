import React, { useState, useEffect } from "react";
import { Nav } from "react-bootstrap";
import Posts from "./Posts";
import { useDispatch, useSelector } from "react-redux";
import Message from "../components/Message";
import { getPosts, getLikedPosts } from "../actions/postActions";

// Content of home page; tabs to select which list of posts to view
function HomeContent() {
  const dispatch = useDispatch();

  const [tab, setTab] = useState(1);

  const getLiked = useSelector((state) => state.getLiked);
  const { error: getLikedError, response } = getLiked;

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const postList = useSelector((state) => state.postList);
  const { error, success, post } = postList;

  useEffect(() => {
    if (response == null) {
      dispatch(getLikedPosts());
    }
    if (post == null) {
      dispatch(getPosts());
    }
  }, [dispatch, response, post]);

  const [message, setMessage] = useState("");
  const likedPosts = response ? response.items : [];
  const posts = post ? post.items : [];

  // is this posted by me?
  const isMyPost = (p) => {
    let idList = p.author.id.split("/");
    let id = "";
    for (let i = 0; i < idList.length; i++) {
      if (idList[i] == "author") {
        id = idList[i + 1];
        break;
      }
    }
    if (id == userInfo.author_id) {
      return true;
    } else {
      return false;
    }
  };

  return (
    <div className="m-2">
      {message && <Message variant="danger">{message}</Message>}
      {error && <Message variant="danger">{error}</Message>}
      {getLikedError && <Message variant="danger">{getLikedError}</Message>}
      <Nav fill variant="tabs" defaultActiveKey="1">
        <Nav.Item>
          <Nav.Link eventKey="1" onClick={() => setTab(1)}>
            All Posts
          </Nav.Link>
        </Nav.Item>
        <Nav.Item>
          {userInfo ? (
            <Nav.Link eventKey="2" onClick={() => setTab(2)}>
              Friend Posts
            </Nav.Link>
          ) : (
            <Nav.Link eventKey="2" disabled>
              Friend Posts
            </Nav.Link>
          )}
        </Nav.Item>
        <Nav.Item>
          {userInfo ? (
            <Nav.Link eventKey="3" onClick={() => setTab(3)}>
              My Posts
            </Nav.Link>
          ) : (
            <Nav.Link eventKey="3" disabled>
              My Posts
            </Nav.Link>
          )}
        </Nav.Item>
      </Nav>
      {tab === 1
        ? likedPosts &&
          posts.map((p) =>
            userInfo != null ? (
              <Posts post={p} liked={likedPosts} />
            ) : p.visibility == "PUBLIC" ? (
              <Posts post={p} liked={likedPosts} />
            ) : (
              ""
            )
          )
        : tab === 2
        ? likedPosts &&
          posts.map((p) =>
            p.visibility == "FRIENDS" && !isMyPost(p) ? (
              <Posts post={p} liked={likedPosts} />
            ) : (
              ""
            )
          )
        : likedPosts &&
          posts.map((p) =>
            isMyPost(p) ? <Posts post={p} liked={likedPosts} /> : ""
          )}
    </div>
  );
}
export default HomeContent;
