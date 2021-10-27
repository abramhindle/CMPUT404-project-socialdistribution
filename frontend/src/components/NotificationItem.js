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

    archiveRequest(){
        return(<div></div>);
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
                    {this.props.item.summary}
                    </Card.Text>
                    <Col className="m-auto" style={{width:"50rem"}}>
                        <Button className="m-1" style={{width:"10rem"}} variant={this.state.isToggleOn ? 'success':'danger'} 
                            onClick={this.handleClick}> {this.state.isToggleOn ? 'Follow him/her' : 'Unfollow him/her'}
                        </Button>
                        <Button 
                        className="m-1" style={{width:"10rem"}} variant="warning" onClick={this.archiveRequest}>
                            Archive</Button>
                            {/* delete the notification from database */}

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