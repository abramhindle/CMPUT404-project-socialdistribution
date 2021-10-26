import React from "react";

import { Container, Row, Col, Card, Alert, Button} from "react-bootstrap";
import Headers from "../components/Headers";
import SideBar from "../components/SideBar";
import HomePost from "../components/HomePost";


function NotificationPage() {
    
    // get FriendRequest data from db
    // const [id, setId] = useState("");
    // const [summary, setSummary] = useState("");
    // const [requestor, setRequestor] = useState("");
    // const [requestee, setAuthor] = useState(""); // this is the author
    
    return (

        <Container className="App fluid min-vh-100 min-vw-100 d-flex flex-column p-0">
        <Headers />
        <Row className="flex-grow-1 m-0">
            <Col className="bg-secondary col-md-2 border">
                <SideBar />
            </Col>
            <Col>
                {/* <div>
                <Form className="justfiy-content-center align-center">
                <Form.Group className="m-3" controlId="title">
                    <Form.Label>Title</Form.Label>
                    <Form.Control type="title" placeholder="Title here" />
                </Form.Group>
                <Form.Group className="m-3" controlId="description">
                    <Form.Label>Description</Form.Label>
                    <Form.Control as="textarea" rows={5} />
                </Form.Group>
                <div className="d-flex align-items-end justify-content-end px-5">
                    <Button className="btn" type="submit" variant="primary">
                    Submit
                    </Button>
                </div>

                </Form>
                </div> */}
                <div>
                <Alert className="m-1" variant="info">
                    New Followers
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
                        <Button className="m-1" style={{width:"7rem"}} variant="success">Follow back</Button>
                        <Button className="m-1" style={{width:"7rem"}} variant="warning">Archieve</Button>
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
                    Hello, I'm Test2! Can I be your follower?
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        <Button className="m-1" style={{width:"7rem"}} variant="success">Follow back</Button>
                        <Button className="m-1" style={{width:"7rem"}} variant="warning">Archive</Button>
                    </Col>
                </Card.Body>
                </Card>
                </div>
                
            </Col>
        </Row>
        </Container>
        );
}

export default NotificationPage;
