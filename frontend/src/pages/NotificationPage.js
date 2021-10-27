import React from "react";

import { Container, Row, Col, Card, Alert, Button} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import HomePost from "../components/HomePost";
import NotificationItem from "../components/NotificationItem"


function NotificationPage() {
    
    // get FriendRequest data from db
    // const [id, setId] = useState("");
    // const [summary, setSummary] = useState("");
    // const [requestor, setRequestor] = useState("");
    // const [requestee, setAuthor] = useState(""); // this is the author

    const items = [
        {requestor:"", requestee:"", display_name: "TestUser1", summary: "Hello, I'm Test1!"},
        {requestor:"", requestee:"", display_name: "TestUser2", summary: "Hello, I'm Test2! Do you wanna follow me as well?"}
    ]
    var itemList = []
    for(let item of items){
        itemList.push(<NotificationItem item={item}/>)
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
                {itemList}
                </div>
                
            </Col>
        </Row>
        </Container>
        );
}

export default NotificationPage;
