import React from "react";
import { Navbar, Nav, Card, Button, ButtonGroup, Stack } from "react-bootstrap";
import home_icon from"../images/home.png"
import message_icon from "../images/message.png";
import notification_icon from "../images/notification.png";
import person_icon from "../images/person.png";
import post_icon from "../images/post.png";
import { LinkContainer } from "react-router-bootstrap";
import search_icon from "../images/search.png"

import jQuery from "jquery";

function SideBar() {
  return (
    <Navbar bg="secondary" className="justify-content-center">
      <Nav defaultActiveKey="/home" className="flex-column">

        <Stack gap={2} className="col-md-10 mx-auto" style={{ width: "10px" }}>
        <LinkContainer
            to="/"
            className="m-1"
            style={{ width: "180px" }}
            variant="success"
          >
            <Button>
              <img
                src={home_icon}
                style={{ width: "20px", marginRight: "5px" }}
              ></img>
              Home
            </Button>
          </LinkContainer>

          <LinkContainer
            to="/notification"
            className="m-1"
            style={{ width: "180px" }}
            variant="warning"
          >
            <Button>
              <img
                src={notification_icon}
                style={{ width: "20px", marginRight: "5px" }}
              ></img>
              Notifications
            </Button>
          </LinkContainer>

          <LinkContainer
            to="/followers"
            className="m-1"
            style={{ width: "180px" }}
            variant="info"
          >
            <Button>
              <img
                src={person_icon}
                style={{ width: "20px", marginRight: "5px" }}
              ></img>
              My Followers
            </Button>
          </LinkContainer>

        </Stack>
      </Nav>
    </Navbar>
  );
}

export default SideBar;