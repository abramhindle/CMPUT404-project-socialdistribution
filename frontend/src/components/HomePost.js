import React from "react";
import { Navbar, Nav, Card, Button, ButtonGroup, Row, Col, Dropdown, DropdownButton} from "react-bootstrap";

import Headers from "./Headers";
import "./HomePost.css";
import Avatar from "../images/avatar.jpg";

function HomePost() {
  return (
    <div class="HomePost">
      <div class="tweet">
        <div class="tweet__column avatar">
          <img class="avatar__image" src={Avatar} />
        </div>
        <div class="tweet__column tweet__main">
          <div class="tweet__main__header">
            <div class="tweet__main__header__item tweet__main__header__item--name">
              BlahX
            </div>
            <div class="tweet__main__header__item tweet__main__header__item--handle">
              @blahx
            </div>
            <div class="tweet__main__header__item tweet__main__header__item--duration">
              7h
            </div>
          </div>
          <div class="tweet__main__message">
            Blah blah blah Blah blah blah
            <br />
            Blah blah blah
          </div>
          <div class="tweet__footer">
            <div class="tweet__footer__stats">
              <img
                class="tweet__icon tweet__footer__stats__item"
                src="http://educative.io/udata/nWjylg5XloB/footer_icon.svg"
              />
              <div class="tweet__footer__stats__item">likes: 10</div>
            </div>
            <div class="tweet__footer__stats">
              <img
                class="tweet__icon tweet__footer__stats__item"
                src="http://educative.io/udata/nWjylg5XloB/footer_icon.svg"
              />
              <div class="tweet__footer__stats__item">comments: 900</div>
            </div>
          </div>
        </div>
        <div class="tweet__menu">
          <img
            class="tweet__icon tweet__menu__icon"
            src="http://educative.io/udata/w66j6pMjng6/down_icon.svg"
          />
        </div>
      </div>

      <div class="tweet">
        <div class="tweet__column avatar">
          <img class="avatar__image" src={Avatar} />
        </div>
        <div class="tweet__column tweet__main">
          <div class="tweet__main__header">
            <div class="tweet__main__header__item tweet__main__header__item--name">
              BlahX
            </div>
            <div class="tweet__main__header__item tweet__main__header__item--handle">
              @blahx
            </div>
            <div class="tweet__main__header__item tweet__main__header__item--duration">
              7h
            </div>
          </div>
          <div class="tweet__main__message">
            Blah blah blah Blah blah blah
            <br />
            Blah blah blah
          </div>
          <div class="tweet__footer">
            <div class="tweet__footer__stats">
              <img
                class="tweet__icon tweet__footer__stats__item"
                src="http://educative.io/udata/nWjylg5XloB/footer_icon.svg"
              />
              <div class="tweet__footer__stats__item">likes: 10</div>
            </div>
            <div class="tweet__footer__stats">
              <img
                class="tweet__icon tweet__footer__stats__item"
                src="http://educative.io/udata/nWjylg5XloB/footer_icon.svg"
              />
              <div class="tweet__footer__stats__item">comments: 900</div>
            </div>
          </div>
        </div>
        <div class="tweet__menu">
          <img
            class="tweet__icon tweet__menu__icon"
            src="http://educative.io/udata/w66j6pMjng6/down_icon.svg"
          />
        </div>
      </div>
      
      <Card style={{width:"60rem"}}>
          <Card.Body> 
            <div className="d-flex">
              
            <Card.Img src={Avatar} style={{width: "6rem", height: "6rem"}}/>
            
            <Card.Title className="justify-content-center">BlahX</Card.Title>
            <Card.Subtitle className="mb-2 text-muted">
              @BlahX
            </Card.Subtitle>


            </div>
            <Card.Text>
              Some quick example text to build on the card title and make up the
              bulk of the card's content.
            </Card.Text>
          
            <Col className="m-auto" style={{width:"50rem"}}>
              <Button className="m-1" style={{width:"7rem"}} variant="success">Like</Button>
              <Button className="m-1" style={{width:"7rem"}} variant="info">Comment</Button>
              <Button className="m-1" style={{width:"7rem"}} variant="warning">Share</Button>
    
            </Col>
            
            
          </Card.Body>
        </Card>
    </div>

  );
}
export default HomePost;
