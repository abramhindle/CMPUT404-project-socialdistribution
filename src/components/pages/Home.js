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
        password1: '',
        password2: '',
        // passwordFeedback: 'False'
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
      fetch('http://127.0.0.1:8000/service/auth/register/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
      },
      body: JSON.stringify(userModal)
    })
    .then(res => {let a = res.json(); console.log(a)})
    .then(data => {
      console.log(data)
      if (data === undefined) {
        alert("Your account has been created. You'll be able to log in when it is activated!")
      }
      if (data?.key) {
        localStorage.clear();
        localStorage.setItem('token', data.key);
        // Fix replace
        window.location.replace('http://localhost:3000/dashboard');
      } 
      // else {
      //   setEmail('');
      //   setPassword('');
      //   localStorage.clear();
      //   setErrors(true);
      // }
    })
    .catch(errors => console.log(errors));     
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
                <Form.Control required minLength="8" onChange={handleChange} name="password1" value={userModal.password1}  type="password" placeholder="Password" />
                <Form.Control.Feedback type='invalid'>Invalid Input!!</Form.Control.Feedback>
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control required minLength="8" onChange={handleChange} name="password2" value={userModal.password2} type="password" placeholder="Confirm Password" />
                <Form.Control.Feedback type='invalid'>Invalid Input!</Form.Control.Feedback>
            </Form.Group>
        </Form>

        <div className="flex-row-reverse">
                <Button className="pl-5" variant="primary" type="submit" onClick={props.onHide,handleSignUP}>Sign Up</Button>
            </div>

      </Modal.Body>
      </Modal>
    );
  }



/// LOGIN MODAL
function LogInModal(props) {
  const [loading, setLoading] = React.useState(true);
    const [userModal, setuserModal] = React.useState({
      email:'',
      password: '',
  });
  React.useEffect(() => {
    if (localStorage.getItem('token') !== null) {
      window.location.replace('http://localhost:3000/dashboard');
    } else {
      setLoading(false);
    }
  }, []);

  function handleChange(e){
    setuserModal({...userModal, [e.target.name]: e.target.value})
}  
  function handleLogIn(){
    fetch('http://127.0.0.1:8000/service/auth/login/', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
      },
      body: JSON.stringify(userModal)
    })

  .then(res => res.json())
  .then(data => {
    if (data.key) {
      localStorage.clear();
      localStorage.setItem('token', data.key);
      // Fix replace
      window.location.replace('http://localhost:3000/dashboard');
    } 
    // else {
    //   setEmail('');
    //   setPassword('');
    //   localStorage.clear();
    //   setErrors(true);
    // }
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
                <Form.Label>Email</Form.Label>
                <Form.Control required onChange={handleChange} name='email' type="email" value={userModal.email} placeholder="Email" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Password</Form.Label>
                <Form.Control required minLength="8" onChange={handleChange} name='password' type="password" value={userModal.password} placeholder="Password" />
            </Form.Group>
        </Form>
        <div className="me-auto">
              <Button variant="primary" type="submit" onClick={props.onHide, handleLogIn}>Log In</Button>
          </div>     
      </Modal.Body>
      </Modal>
    );
  }

export default Home;
