import React from "react";

import { Container, Row, Col, Card, Alert, Button} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import HomeContent from "../components/HomeContent";
import NotificationItem from "../components/NotificationItem"


function NotificationPage() {
    
    // get FriendRequest data from db
    // const [id, setId] = useState("");
    // const [summary, setSummary] = useState("");
    // const [requestor, setRequestor] = useState("");
    // const [requestee, setAuthor] = useState(""); // this is the author

    const items = [
        {message_type:"", requestor:"", requestee:"", display_name: "TestUser1", summary: "Hello, I'm Test1!"},
        
        {message_type:"", requestor:"", requestee:"", display_name: "TestUser2", summary: "Hello, I'm Test2! Do you wanna follow me as well?"}
    ]
    var itemList = []
    for(let item of items){
        itemList.push(<NotificationContent item={item}/>)
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
            {/* {tab === 1
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
                )} */}
                
                        {itemList}
                        </div>
                
            </Col>
        </Row>
        </Container>
        );
}

export default NotificationPage;