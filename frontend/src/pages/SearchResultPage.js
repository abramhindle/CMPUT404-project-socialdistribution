import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form, Stack, Alert } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import searchicon from "../images/search.png";
import { useDispatch, useSelector } from "react-redux";
import { LinkContainer } from "react-router-bootstrap";
import SearchResultItem from "../components/SearchResults";
import { getPosts } from "../actions/postActions";
import { getUsers } from "../actions/userActions";
import Posts from "../components/Posts";

const SearchResultPage = (props) => {


  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const postList = useSelector((state) => state.postList);
  const { post } = postList;

  // get user list
  const userList = useSelector((state) => state.userList);
  useEffect(() => {
    dispatch(getUsers());
  }, [dispatch]);
  console.log(userList.userList);

  //console.log(props.match.params.id);
  const searchText = props.match.params.id;

  useEffect(() => {
    if (post == null) {
      dispatch(getPosts());
    }
  }, [dispatch, post]);

  const [message, setMessage] = useState("");
  const posts = post ? post.items : [];

  var searchResultPosts = [];

  for( var i=0;i<posts.length;i++){ 
    if ( posts[i].title.indexOf(searchText) != -1) {
      searchResultPosts.push(posts[i]);
    }
  }



  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers />
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col>
                <div>
                <Alert className="m-1" variant="info">
                  Search Results
                </Alert>    
                </div>
                <Alert>hahaha</Alert>
                {searchResultPosts.map((p) => (
                  <Posts post={p} />
                ))}
        </Col>
      </Row>
    </Container>
  );
}

export default SearchResultPage;
