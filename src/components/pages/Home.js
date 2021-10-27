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


/// SIGNUP MODAL
function SignUpModal(props) {
    const [validated, setValidated] = React.useState(false);
    const [userModal, setuserModal] = React.useState({
        email:'',
        username: '',
        password: '',
        password2: '',
        passwordFeedback: 'False'
    });

    const handleSubmit = (event) => {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        setValidated(true);
    };


    function handleChange(e){
        setuserModal({...userModal, [e.target.name]: e.target.value})
    }
    function handleSignUP(){
        console.log(userModal)
        const url = 'http://localhost:8000/service/accounts/';
        const options = {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8'
        },
        body: JSON.stringify(userModal)
    };
        
        fetch(url, options)
          .then(response => {
            //   response.status == '200'
            console.log(response.auth);
          });
    }

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
       
        <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>Email</Form.Label>
                <Form.Control required onChange={handleChange} name="email" value={userModal.email} type="email" placeholder="Email"/>
                <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
                <Form.Text className="text-muted">
                We'll never share your email with anyone else.
                </Form.Text>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Username</Form.Label>
                <Form.Control required onChange={handleChange} name="username" value={userModal.username} type="text" placeholder="Username" />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control required minLength="8" onChange={handleChange} name="password" value={userModal.password}  type="password" placeholder="Password" />
                <Form.Control.Feedback type='invalid'>Invalid Input!!</Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control required minLength="8" onChange={handleChange} name="password2" value={userModal.password2} type="password" placeholder="Confirm Password" />
                <Form.Control.Feedback type='invalid'>Invalid Input!</Form.Control.Feedback>
            </Form.Group>
        </Form>
            <hr></hr>
            <div className="me-auto">
                <Button class="mr-1" variant="primary" type="submit" onClick={props.onHide,handleSignUP}>Sign Up</Button>
            </div>
      </Modal.Body>
      </Modal>
    );
  }



/// LOGIN MODAL
function LogInModal(props) {
    const [userModal, setuserModal] = React.useState({

    });
    function handleLogIN(){
        const url = 'http://localhost:8000/service/accounts/';
        const options = {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8'
          },
          body: JSON.stringify({
            a: 10,
            b: 20
          })
        };
        
        fetch(url, options)
          .then(response => {
            console.log(response.status);
          });
    }

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
          <Button variant="primary" type="submit" onClick={props.onHide, handleLogIN}>Log In</Button>
        </Modal.Footer>
      </Modal>
    );
  }

export default Home;
