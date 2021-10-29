import React from 'react'
import {Row,Col,Button, Container, Modal, Form, Image, Ratio, Card} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import './Author.css'
import { faHeart, faComment, faThumbsUp, faShare } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from "@fortawesome/free-brands-svg-icons"
import { useParams } from "react-router-dom";

function Author ()  {
    let {id} = useParams();
    const [loading, setLoading] = React.useState(true);
    const [author, setAuthor] = React.useState({});
    const [editState, setEdit] = React.useState(false);

    function handleChange(e){
        setAuthor({...author, [e.target.name]: e.target.value})
    }  

    React.useEffect(() => {
      if (localStorage.getItem('token') === null) {
        window.location.replace('http://localhost:3000/');
      } else {
        fetch(`http://127.0.0.1:8000/service/author/${id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${localStorage.getItem('token')}`
          }
        })
          .then(response => response.json())
          .then((response) => {
              setAuthor(response);
              setLoading(false);
  
          })
      }
    },[]
    );

    // Endpoint
    function submitEdit(){
        if (editState){
            fetch(`http://127.0.0.1:8000/service/author/${id}`, {
                method: 'POST',
                headers: {
                  'Accept': 'application/json',
                  'Content-Type': 'application/json;charset=UTF-8'
                },
                body: JSON.stringify(author),
              })
              .then(res => {let a = res.json(); console.log(a)})
              .then(data => {
                console.log(data,'TESTT')
                if (data?.key) {
                  localStorage.clear();
                  localStorage.setItem('token', data.key);
                  // Fix replace
                //   window.location.replace('http://localhost:3000/dashboard');
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
      setEdit(!editState)
      }
      
    function setLogout(){
      localStorage.clear();
      window.location.reload();
      console.log('logout')
    }

    return (
      <React.Fragment>      
                <Row>
                    <Col className='Authors-leftCol p-5' xs={3}>
                      <Ratio aspectRatio='1x1'>
                          <Image className='fluid' src={author.profileImage} roundedCircle />
                        </Ratio>
                     <h3>Welcome <br></br>{author.displayName}</h3>
                      <div><a className='Authors-leftColLink' href={author.github}>Create Post</a></div>
                      <div><a className='Authors-leftColLink' href={author.github}>Settings</a></div>
                      <div><a className='Authors-leftColLink'  onClick={ () =>setLogout()}>Logout</a></div>
                    </Col>
                    <Col className='Authors-rightCol Authors-hWhite ps-5 pt-4'  xs={9}>
                    <div>
                      {loading === false && (
                        <React.Fragment>
                          <h1 className='Authors-leftColLink'>@{author.displayName} <Button onClick={submitEdit} variant={editState ? 'success' : 'link'}>{editState ? 'Save' : 'Edit Profile'}</Button> </h1>   
                            <Card className = 'Card my-5'>
                            <Card.Body>
                              <Card.Title>
                                <div>
                                {editState ? 
                                    <Form.Group className="mb-3" controlId="userGithub">
                                        <Form.Label>Github</Form.Label>
                                        <Form.Control size='md' required onChange={handleChange} name="github" value={author.github} type="text" placeholder="Github" />
                                    </Form.Group>
                                 : <div><h1><p>Github <a href={author.github}><FontAwesomeIcon icon={faGithub}/></a></p></h1> <p>{author.github}</p> </div>}
                                </div>
                                <div>
                                {editState ? 
                                    <Form.Group className="mb-3" controlId="userGithub">
                                        <Form.Label>Username</Form.Label>
                                        <Form.Control size='md' required onChange={handleChange} name="displayName" value={author.displayName} type="text" placeholder="Display Name" />
                                    </Form.Group>
                                 : <div><h1><p>Username</p></h1> <p>{author.displayName}</p> </div>}
                                </div>
                                <div>
                                {editState ? 
                                    <Form.Group className="mb-3" controlId="userGithub">
                                        <Form.Label>Profile Image</Form.Label>
                                        <Form.Control size='md' required onChange={handleChange} name="profileImage" value={author.profileImage} type="text" placeholder="Profile Image" />
                                    </Form.Group>
                                 : <div><h1><p>Profile Image</p></h1>  <p>{author.github}</p> </div>}
                                </div>
                              </Card.Title>
                            </Card.Body>
                          </Card>                 
                      </React.Fragment>
                      )}
                    </div>
                    </Col>
                </Row>
        </React.Fragment>
    );
  }
  
  export default Author;
  
  
  