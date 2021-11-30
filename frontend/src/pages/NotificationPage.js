import React,{useState, useEffect, Component} from 'react';
import { useHistory } from "react-router-dom";

import { Container, Nav, Row, Col, Card, Alert, Button} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import HomeContent from "../components/HomeContent";
import NotificationContent from "../components/NotificationContent"

import { useDispatch, useSelector } from "react-redux";
import { authorFriendlist } from "../actions/userActions";
import { getPosts } from "../actions/postActions";


function NotificationPage() {
    
    // get FriendRequest data from db
    // const [id, setId] = useState("");
    // const [summary, setSummary] = useState("");
    // const [requestor, setRequestor] = useState("");
    // const [requestee, setAuthor] = useState(""); // this is the author
    let history = useHistory();

    const userLogin = useSelector((state) => state.userLogin);
    const { userInfo } = userLogin;
  
    useEffect(() => {
      // redirect user to homepage if user is not logged in
      if (!userInfo) {
        history.push("/login");
      }
    }, [history, userInfo]);

    const [tab, setTab] = useState(1);

    const items = [
        {message_type:"friend_request", sender:"friend1"},
        
        {message_type:"friend_request", sender:"friend2"}
    ]
    const items2 = [
        {message_type:"like", postId:"", sender:"likeTest1"},
        
        {message_type:"like", postId:"", sender:"likeTest2"}

    ]
    const items3 = [
        {message_type:"comment", postId:"", sender:"commentTest1", content: "great information!"},
        
        {message_type:"comment", postId:"", sender:"commentTest2", content: "your post is funny!"}
    ]
    

    var friendRequestList = []
    for(let item of items){
        friendRequestList.push(<NotificationContent item={item}/>)
    }
    var likeList = []
    for(let item of items2){
        likeList.push(<NotificationContent item={item}/>)
    }
    var commentList = []
    for(let item of items3){
        commentList.push(<NotificationContent item={item}/>)
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
                New Notifications
            </Alert>    
            <Nav fill variant="tabs" defaultActiveKey="1">
            
            <Nav.Item className="m-1">
            {userInfo ? ( // change to if there's new notif?
                <Nav.Link eventKey="1" onClick={() => setTab(1)}>
                Friend Requests
                </Nav.Link>
            ) : (
                <Nav.Link eventKey="1" onClick={() => setTab(1)}>
                Friend Requests
                </Nav.Link>
            )}
            </Nav.Item>
            
            <Nav.Item>
            {userInfo ? ( // change to if there's new notif?
                <Nav.Link eventKey="2" onClick={() => setTab(2)}>
                Likes
                </Nav.Link>
            ) : (
                <Nav.Link eventKey="2" onClick={() => setTab(2)}>
                Likes
                </Nav.Link>
            )}
            </Nav.Item>
            <Nav.Item>
            {userInfo ? (
                <Nav.Link eventKey="3" onClick={() => setTab(3)}>
                Comments
                </Nav.Link>
            ) : (
                <Nav.Link eventKey="3" onClick={() => setTab(3)}>
                Comments
                </Nav.Link>
            )}
            </Nav.Item>
            </Nav>
            {tab === 1 ? 
                friendRequestList
                : tab === 2 ? 
                likeList
                : 
                commentList}
            
            {/* {friendRequestList} */}
            </div>
                
            </Col>
        </Row>
        </Container>
        );
}

export default NotificationPage;