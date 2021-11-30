import React,{useState, useEffect, Component} from 'react';
import { Container,Nav,Row, Col, Card, Alert, Button, LinkContainer} from "react-bootstrap";
import Posts from "./Posts";
import { useDispatch, useSelector } from "react-redux";
import { authorFriendlist } from "../actions/userActions";
import Message from "./Message";
import { getPosts } from "../actions/postActions";

function NotificationContent(prop) {
    const dispatch = useDispatch();

    const [tab, setTab] = useState(1);

    const userDetail = useSelector((state) => state.userDetail);
    const { error, loading, userInfo } = userDetail;

    useEffect(() => {
        if (userInfo == null) {
        dispatch(authorFriendlist());
        }
    }, [dispatch, userInfo]);
    
    // TODO: this should be user request passed in
    console.log(prop.post);

    // handleClick() {
    //     this.setState(prevState => ({
    //       isToggleOn: !prevState.isToggleOn
    //     }));
    // }

  
    return(
        <div>
          
        <Col>
            <div className="item">
            <Card className="m-1" style={{ width: '30rem' }}>
            <Card.Body>
                <div className="d-flex">
                    <Card.Title></Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">@</Card.Subtitle>
                </div>
                <Card.Text>
                
                </Card.Text>
                <Col className="m-auto" style={{width:"50rem"}}>
                    {/* <Button className="m-1" style={{width:"10rem"}} variant={state.isToggleOn ? 'success':'danger'} 
                        onClick={handleClick}> {state.isToggleOn ? 'Follow him/her' : 'Unfollow him/her'}
                    </Button> */}
                    <Button 
                    className="m-1" style={{width:"10rem"}} variant="warning">
                        Archive</Button>
                        {/* delete the notification from database */}

                </Col>
            </Card.Body>
            </Card>
            </div>
        </Col>
        </div>
    );
  }
  export default NotificationContent;
  

//   <Col>
//             <div className="item">
//             <Card className="m-1" style={{ width: '30rem' }}>
//             <Card.Body>
//                 <div className="d-flex">
//                     <Card.Title>{props.item.display_name}</Card.Title>
//                     <Card.Subtitle className="mb-2 text-muted">@{props.item.display_name}</Card.Subtitle>
//                 </div>
//                 <Card.Text>
//                 {this.props.item.summary}
//                 </Card.Text>
//                 <Col className="m-auto" style={{width:"50rem"}}>
//                     <Button className="m-1" style={{width:"10rem"}} variant={state.isToggleOn ? 'success':'danger'} 
//                         onClick={handleClick}> {state.isToggleOn ? 'Follow him/her' : 'Unfollow him/her'}
//                     </Button>
//                     <Button 
//                     className="m-1" style={{width:"10rem"}} variant="warning" onClick={archiveRequest}>
//                         Archive</Button>
//                         {/* delete the notification from database */}

//                 </Col>
//             </Card.Body>
//             </Card>
//             </div>
//         </Col>