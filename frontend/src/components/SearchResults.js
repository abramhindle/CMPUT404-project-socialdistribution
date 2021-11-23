import React,{Component} from 'react';
import { Container, Row, Col, Card, Alert, Button, LinkContainer} from "react-bootstrap";


class SearchResultItem extends Component{
    constructor(props) {
        super(props);
        
    }
    

      
    render(){

        return(
            <div>
            <Col>
                <div className="item">
                <Card className="m-1" style={{ width: '30rem' }}>
                <Card.Body>
                    <div className="d-flex">
                        <Card.Title>{this.props.item.title}</Card.Title>
                        <Card.Subtitle className="mb-2 text-muted">@{this.props.item.author}</Card.Subtitle>
                    </div>
                    
                    <Col className="m-auto" style={{width:"50rem"}}>
                        <Alert style={{width:"28rem", backgroundColor:"white", color:"black"}}>{this.props.item.textContent}</Alert>
                        <Button className="m-1" style={{width:"5rem"}} variant="success">View</Button>

                    </Col>
                </Card.Body>
                </Card>
                </div>
            </Col>
            </div>
        )
    }
}

export default SearchResultItem