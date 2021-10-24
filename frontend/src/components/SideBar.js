import React from "react";
import { Navbar, Nav, Card, Button, ButtonGroup, Dropdown, DropdownButton} from "react-bootstrap";

function SideBar() {
  return (
    <Navbar bg="secondary" className="justify-content-center">
      <Nav defaultActiveKey="/home" className="flex-column">
        <Card>
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
        </Card>
        {/* <Card className="m-auto" style={{ width: "14rem", borderRadius:"1rem", borderBlock:"groovy", }} >
          <Card.Body className="m-auto">
              <Button variant="outline-success" size="lg">Post</Button>
          </Card.Body>
        </Card>
        <Card className="m-auto" style={{ width: "14rem", borderRadius:"1rem"}} >
          <Card.Body className="m-auto">
              <Button variant="outline-warning" size="lg">More</Button>  
              <Button variant="outline-warning" size="lg">My Post</Button>        
          </Card.Body>
        </Card> */}
        <ButtonGroup vertical className="m-auto" style={{width:"10rem"}}>
          <Button className="m-1" variant="success">Add Post</Button>
          
          <Button className="m-1" variant="warning">More</Button>
        </ButtonGroup>

        <Nav.Link href="/home">Active</Nav.Link>
        <Nav.Link eventKey="link-1">Link</Nav.Link>
        <Nav.Link eventKey="link-2">Link</Nav.Link>
        <Nav.Link eventKey="disabled" disabled>
          Disabled
        </Nav.Link>
    
      </Nav>
    </Navbar>
  );
}

export default SideBar;
