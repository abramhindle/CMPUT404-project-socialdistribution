import React from 'react'
import { Row, Col, Button, Container } from 'react-bootstrap';
import SignUpModal from '../components/SignUpModal';
import LogInModal from '../components/LogInModal';
import { useUserHandler } from "../UserContext"
import { useHistory } from "react-router-dom"
import './Home.css'


function Home ()  {
    const [modalShowSignUp, setModalShowSignUp] = React.useState(false);
    const [modalShowLogIn, setModalShowLogIn] = React.useState(false);
    const { setLoggedInUser } = useUserHandler()

    // redirect away from the Home page with useHistory
    const history = useHistory()

    React.useEffect(() => {
      if ((localStorage.getItem('token') !== null) 
        && (localStorage.getItem('user') !== null)) {
          setLoggedInUser(JSON.parse(localStorage.getItem('user')));
          history.push(`/stream`)
      }
    }, [setLoggedInUser, history]);

    return (
        <React.Fragment>      
            <Row style={{height: "100vh", margin: "0"}}>
                <Col className='Home-leftCol d-none d-sm-block' xs={0} sm={5} lg={7}></Col>
                <Col className='Home-rightCol Home-hWhite' xs={12} sm={7} lg={5}>
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
                                <Button className='col-12' variant="primary" onClick={() => setModalShowLogIn(true)}>
                                    Log In
                                </Button>
                                <LogInModal
                                    show={modalShowLogIn}
                                    onHide={() => setModalShowLogIn(false)}
                                    closeModal={() => setModalShowLogIn(false)}
                                />
                            </Col>
                            <Col xs={6}>
                                <Button className='col-12' variant="secondary" onClick={() => setModalShowSignUp(true)}>
                                    Sign Up
                                </Button>
                                <SignUpModal
                                    show={modalShowSignUp}
                                    onHide={() => setModalShowSignUp(false)}
                                    closeModal={() => setModalShowSignUp(false)}
                                />
                            </Col>
                        </Row>
                    </div></Container>
                        
                </Col>
            </Row>
        </React.Fragment>
    )
}

export default Home;
