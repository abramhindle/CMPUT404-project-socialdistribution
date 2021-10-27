import React from 'react'
import {Row,Col,Button, Container, Modal, Form} from 'react-bootstrap';
import './Home.css'


function Home ()  {
    const [modalShowSignUp, setModalShowSignUp] = React.useState(false);
    const [modalShowLogIn, setModalShowLogIn] = React.useState(false);
    return (
        <React.Fragment>      
                <Row>
                    <Col className='Home-leftCol' xs={7}></Col>
                    <Col className='Home-rightCol Home-hWhite'  xs={5}>
                        <Container className='Home-rightCont'>
                        <div>
                            <h1 ><strong>Plurr</strong></h1>
                            <h2><strong>Stay connected with friends and the world.</strong></h2>
                        </div>
                        <div>
                            <b>Join Today</b>
                        </div>
                    <div className="mb-2 pt-3">
                        <Row>
                            <Col xs={6}>
                                <Button className='col-12 ' variant="primary" onClick={() => setModalShowLogIn(true)}>
                                    Log In
                                </Button>
                                <LogInModal
                                    show={modalShowLogIn}
                                    onHide={() => setModalShowLogIn(false)}
                                />
                            </Col>
                            <Col xs={6}>
                                <Button pt-5 className='col-12' variant="secondary" onClick={() => setModalShowSignUp(true)}>
                                    Sign Up
                                </Button>
                                <SignUpModal
                                    show={modalShowSignUp}
                                    onHide={() => setModalShowSignUp(false)}
                                />
                            </Col>
                        </Row>
                    </div></Container>
                            
                        </Col>
                </Row>
        </React.Fragment>
    )
}

function SignUpModal(props) {
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Create your account
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
       
        <Form>
            <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email</Form.Label>
                <Form.Control type="email" placeholder="Email" />
                <Form.Text className="text-muted">
                We'll never share your email with anyone else.
                </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Username</Form.Label>
                <Form.Control type="password" placeholder="Username" />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control type="password" placeholder="Confirm Password" />
            </Form.Group>

        </Form>
      </Modal.Body>
        <Modal.Footer>
          <Button class="mr-1" variant="primary" type="submit" onClick={props.onHide}>Sign Up</Button>
        </Modal.Footer>
      </Modal>
    );
  }

function LogInModal(props) {
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Log into Plurr
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
        
        <Form>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Username</Form.Label>
                <Form.Control type="password" placeholder="Username" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" placeholder="Password" />
            </Form.Group>

        </Form>
      </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" type="submit" onClick={props.onHide}>Log In</Button>
        </Modal.Footer>
      </Modal>
    );
  }

export default Home;
