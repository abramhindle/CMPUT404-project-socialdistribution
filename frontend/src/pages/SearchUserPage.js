import React, { useState, useEffect } from "react";
import { Container, Row, Col, Button, Form, Stack, Alert,Card,Nav } from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import { useDispatch, useSelector } from "react-redux";
import { getPosts } from "../actions/postActions";
import { getUsers } from "../actions/userActions";
import Posts from "../components/Posts";
import { LinkContainer } from "react-router-bootstrap";
import Avatar from "../images/avatar.jpg";

const SearchUserPage = (props) => {


  const dispatch = useDispatch();

  const userLogin = useSelector((state) => state.userLogin);
  const { userInfo } = userLogin;

  const searchText = props.match.params.id;

  const userList = useSelector((state) => state.userList);
  useEffect(() => {
    dispatch(getUsers());
  }, [dispatch]);
  const users = userList.userList ? userList.userList.items : [];

  var searchResultUsers = [];

  if(searchText==" "){
    for(var i=0; i<users.length; i++){
        if(users[i].displayName){
            if(!users[i].profile_img){
                users[i].profil_img=Avatar;
            }
            searchResultUsers.push(users[i]);  
        }  
    }
  }else{
    for(var i=0; i<users.length; i++){
        if(users[i].displayName.indexOf(searchText)!=-1){
            if(!users[i].profile_img){
                users[i].profil_img=Avatar;
            }
          searchResultUsers.push(users[i]);
          
        }
        console.log("haha");
    }
  }


  return (
    <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
      <Headers searchCategory={"user"}/>
      <Row className="flex-grow-1 m-0">
        <Col className="bg-secondary col-md-2 border">
          <SideBar />
        </Col>
        <Col>
                <div>
                <Alert className="m-1" variant="info">
                  Search results for users
                </Alert>    
                </div>
                {searchResultUsers.map((p)=>(
                  <div>
                      <Card>
                        <Card.Body>
                        <Card.Img className="m-1" src={Avatar} style={{ width: "6rem", height: "6rem" }}/>
                        <LinkContainer to= 
                            {{
                                pathname: '/profile/'+p.displayName,
                                state : {"user_id": p.displayName}
                                
                            }}
                            style={{fontSize:"1.5rem"}}>
                            <Nav.Link className="m-2 justify-content-center">
                            {p.displayName}
                            </Nav.Link>
                            </LinkContainer>
                        </Card.Body>
                      </Card>  
                  </div>
                ))}
                
        </Col>
      </Row>
    </Container>
  );
}

export default SearchUserPage;
