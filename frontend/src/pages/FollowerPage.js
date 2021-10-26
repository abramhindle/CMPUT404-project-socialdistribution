import React from "react";

import { Container, Row, Col, Card, Alert, Button} from "react-bootstrap";
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
        {requestor:"", display_name: "TestUser1", summary: "Hello, I'm Test1!"},
        {requestor:"", display_name: "TestUser2", summary: "Hello, I'm Test2! Do you wanna follow me as well?"}
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
                <Card className="m-1" style={{ width: '30rem' }}>
                <Card.Body>
                    <div className="d-flex">
                        <Card.Title>TestUser1</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">@TestUser1</Card.Subtitle>
                    </div>
                    <Card.Text>
                    Hello, I'm Test1!
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        <Button className="m-1" style={{width:"10rem"}} variant="success">View his posts</Button>
                        <Button className="m-1" style={{width:"10rem"}} variant="danger">Unfollow him/her</Button>
                    </Col>
                </Card.Body>
                </Card>

                <Card className="m-1" style={{ width: '30rem' }}>
                <Card.Body>
                    <div className="d-flex">
                        <Card.Title>TestUser2</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">@TestUser2</Card.Subtitle>
                    </div>
                    <Card.Text>
                    Hello, I'm Test2! Do you wanna follow me as well?
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        <Button className="m-1" style={{width:"10rem"}} variant="success">View his posts</Button>
                        <Button className="m-1" style={{width:"10rem"}} variant="danger">Unfollow him/her</Button>
                    </Col>
                </Card.Body>
                </Card>
                </div>
                
                {itemList}
                
            </Col>
        </Row>
        </Container>
        );
}

export default NotificationPage;
