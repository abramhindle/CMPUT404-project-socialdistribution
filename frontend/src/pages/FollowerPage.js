import React from "react";

import { Container, Row, Col, Card, Alert, Button, LinkContainer} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import FollowerItem from "../components/FollowerItem"


function NotificationPage() {
    
    // get FriendRequest data from db
    // const [id, setId] = useState("");
    // const [summary, setSummary] = useState("");
    // const [requestor, setRequestor] = useState("");
    // const [requestee, setAuthor] = useState(""); // this is the author
    
    const items = [
        {requestor:"", display_name: "TestUser1"},
        {requestor:"", display_name: "TestUser2"},
    ]
    var itemList = []
    for(let item of items){
        itemList.push(<FollowerItem item={item}/>)
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
                    My Followers
                </Alert>    
                </div>
                {itemList}
            </Col>
        </Row>
        </Container>
        );
}

export default NotificationPage;
