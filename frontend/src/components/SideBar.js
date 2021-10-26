import React from "react";
import { Navbar, Nav, Card, Button, ButtonGroup, Stack, Badge} from "react-bootstrap";
import message_icon from "../images/message.png"
import home_icon from "../images/home.png"
import notification_icon from "../images/notification.png"
import person_icon from "../images/person.png"
import post_icon from "../images/post.png"

import jQuery from "jquery";

function SideBar() {
  return (
    <Navbar bg="secondary" className="justify-content-center">
      <Nav defaultActiveKey="/home" className="flex-column">
        {/* <Card>
          <Card.Body>
            <Card.Title>Card Title</Card.Title>
            <Card.Subtitle className="mb-2 text-muted">
              Card Subtitle
            </Card.Subtitle>
            <Card.Text>
              Some quick example text to build on the card title and make up the
              bulk of the card's content.
            </Card.Text>
            <Card.Link href="#">Card Link</Card.Link>
            <Card.Link href="#">Another Link</Card.Link>
          </Card.Body>
        </Card> */}
        <Stack gap={2} className="col-md-10 mx-auto" style={{width:"10px"}}>
            <Button className="m-1" style={{width:"180px"}} variant="dark" href="/">
              <img src={home_icon} style={{width:"20px",marginRight:"5px"}}></img>
              Home
              <Badge className="m-1" variant="primary" pill>
                0
              </Badge>
            </Button>
            <Button className="m-1" style={{width:"180px"}} variant="success" href="/notification">
              <img src={notification_icon} style={{width:"20px",marginRight:"5px"}}></img>
              Notifications
              <Badge className="m-1" variant="primary" pill>
                0
              </Badge>
            </Button>
            <Button className="m-1" style={{width:"180px"}} variant="warning" href="/myposts">
              <img src={post_icon} style={{width:"20px",marginRight:"5px"}}></img>
              My Posts
              <Badge className="m-1" variant="primary" pill>
                0
              </Badge>
            </Button>
            <Button className="m-1" style={{width:"180px"}} variant="info" href="/followers">
              <img src={person_icon} style={{width:"20px",marginRight:"5px"}}></img>
              My Followers
              <Badge className="m-1" variant="primary" pill>
                0
              </Badge>
            </Button>
            
        </Stack>

        {/* <Nav.Link href="/home">Active</Nav.Link>
        <Nav.Link eventKey="link-1">Link</Nav.Link>
        <Nav.Link eventKey="link-2">Link</Nav.Link>
        <Nav.Link eventKey="disabled" disabled>
          Disabled
        </Nav.Link> */}
    
      </Nav>
    </Navbar>
  );
}

export default SideBar;
