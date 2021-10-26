import React,{Component} from 'react';
import { Container, Row, Col, Card, Alert, Button} from "react-bootstrap";

class FollowerItem extends Component{
    render(){
        return(
            // <div className="item">
            // <div className="item-info">
            //     <span className="item-name">{this.props.item.name}</span>
            //     <span className="item-price"> 
            //          {this.props.item.price}元/{this.props.item.unit}
            //     </span>
            // </div>
            // {/* <Counter/> */}
            // </div>
            <div>
            <Col>
                <div>
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
                
                
            </Col>
            </div>
        )
    }
}

export default FollowerItem