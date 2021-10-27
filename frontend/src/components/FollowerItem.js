import React,{Component} from 'react';
import { Container, Row, Col, Card, Alert, Button, LinkContainer} from "react-bootstrap";


class FollowerItem extends Component{
    constructor(props) {
        super(props);
        this.state = {isToggleOn: true};
        this.handleClick = this.handleClick.bind(this);
    }
    
    handleClick() {
        this.setState(prevState => ({
          isToggleOn: !prevState.isToggleOn
        }));
    }
      
    render(){

        return(
            <div>
            <Col>
                <div className="item">
                <Card className="m-1" style={{ width: '30rem' }}>
                <Card.Body>
                    <div className="d-flex">
                        <Card.Title>{this.props.item.display_name}</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">@{this.props.item.display_name}</Card.Subtitle>
                    </div>
                    <Card.Text>
                    
                    {/* later, we can show author's description/avatar if we have */}
                    {/* {this.props.item.summary} */}

                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        <Button className="m-1" style={{width:"10rem"}} variant="success">View his posts</Button>
                        <Button 
                        className="m-1" style={{width:"10rem"}} variant={this.state.isToggleOn ? 'danger':'success'} onClick={this.handleClick}>
                            {this.state.isToggleOn ? 'Unfollow him/her' : 'Follow him/her'}</Button>

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