import React,{useState, useEffect, Component} from 'react';
import { Container,Nav,Row, Col, Card, Alert, Button, LinkContainer} from "react-bootstrap";
import Posts from "./Posts";
import { useDispatch, useSelector } from "react-redux";
import { authorFriendlist } from "../actions/userActions";
import Message from "./Message";
import { getPosts } from "../actions/postActions";

function NotificationContent(prop) {
    const dispatch = useDispatch();

    const userDetail = useSelector((state) => state.userDetail);
    const { error, loading, userInfo } = userDetail;

    useEffect(() => {
        if (userInfo == null) {
        dispatch(authorFriendlist());
        }
    }, [dispatch, userInfo]);
    
    // TODO: this should be user request passed in
    console.log(prop.item);

    // handleClick() {
    //     this.setState(prevState => ({
    //       isToggleOn: !prevState.isToggleOn
    //     }));
    // }

  
    return(
        <div>
          
        <Col>
            <div className="item">
            <Card className="m-1" style={{ width: '40rem' }}>

            <Card.Body>
                <div className="d-flex">
                    <Card.Title></Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">{prop.item.sender}</Card.Subtitle>
                </div>
                
                
                {prop.item.message_type == "friend_request" ? ( // change to if there's new notif?
                    <div>
                    <Card.Text>
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        {/* <Button className="m-1" style={{width:"10rem"}} variant={state.isToggleOn ? 'success':'danger'} 
                            onClick={handleClick}> {state.isToggleOn ? 'Follow him/her' : 'Unfollow him/her'}
                        </Button> */}
                        <Button className="m-1" style={{width:"10rem"}} variant="success">
                            Accept
                        </Button>
                        <Button className="m-1" style={{width:"10rem"}} variant="danger">
                            Reject
                        </Button>
                    </Col>
                    </div>
                ) : prop.item.message_type == "like" ? 
                (
                    <div>
                    <Card.Text>
                    like your post #post_name!
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        {/* <Button className="m-1" style={{width:"10rem"}} variant={state.isToggleOn ? 'success':'danger'} 
                            onClick={handleClick}> {state.isToggleOn ? 'Follow him/her' : 'Unfollow him/her'}
                        </Button> */}
                        <Button className="m-1" style={{width:"10rem"}} variant="warning">
                            Archive
                        </Button>
                    </Col>
                    </div>
                ) : (
                    <div>
                    <Card.Text>
                    comment your post #post_name : {prop.item.content}
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        {/* <Button className="m-1" style={{width:"10rem"}} variant={state.isToggleOn ? 'success':'danger'} 
                            onClick={handleClick}> {state.isToggleOn ? 'Follow him/her' : 'Unfollow him/her'}
                        </Button> */}
                        <Button className="m-1" style={{width:"10rem"}} variant="warning">
                            Archive
                        </Button>
                    </Col>
                    </div>
                )}
                
            </Card.Body>

            </Card>
            </div>
        </Col>
        </div>
    );
  }
  export default NotificationContent;
  
