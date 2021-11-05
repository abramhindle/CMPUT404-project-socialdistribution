import React from 'react'
import {Row,Col,Button, Container, Modal, Form, Image, Ratio, Card} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeart, faComment, faThumbsUp, faShare } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from "@fortawesome/free-brands-svg-icons"
import PlurrPage from '../components/PlurrPage';


function Stream ()  {
  const [loading, setLoading] = React.useState(true);
  const [items, setItems] = React.useState([]);
  const [isLiked, setLiked] = React.useState(false);

  React.useEffect(() => {
    if (localStorage.getItem('token') === null) {
      window.location.replace('http://localhost:3000/');
    } else {
      fetch('http://127.0.0.1:8000/service/authors/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then(response => response.json())
        .then((response) => {
          console.log(response)
            setItems({items: response.items});
            setLoading(false);

        })
    }
  },[]);

  // send api call with post and userid
  function toggleLiked(postuuid){
    console.log(postuuid)
    setLiked(!isLiked)  
  };

  function likedPost() {
    return  <Button variant="danger"><FontAwesomeIcon style={{color:'black'}} icon={faHeart}/> Liked</Button>;
  }
  
  function unlikedPost() {
    return <Button variant="danger"><FontAwesomeIcon icon={faHeart}/> Like</Button>;
  }

  
  return (    
    <PlurrPage>
      <div>
        {loading === false && (
          <React.Fragment>
            <h1 className='' style={{color: "black"}}> My Plurr Feed</h1>
            {items.items.map((name, count) => (   
              <Card key={count} className='Card my-5' style={{width: "100%"}}>
                {/* <Card.Img variant="top" src="https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png" /> */}
                <Card.Body>
                  <Card.Title>
                    <a href={name.id}>@{name.displayName}</a>
                    <a href={name.github}><FontAwesomeIcon icon={faGithub}/></a>
                  </Card.Title>
                  {/* <Card.Subtitle className="mb-2 text-muted">{name.type}</Card.Subtitle> */}
                  <Card.Text>
                    Example post, a picture of a cat, by a dog
                  </Card.Text>
                    <Button onClick={() => toggleLiked(2)} variant="danger"><FontAwesomeIcon 
                    style={ isLiked ?{color:'black'} : null} icon={faHeart}/> {isLiked? 'Liked' : 'Like'}</Button>
                  <Button variant="primary"> <FontAwesomeIcon icon={faComment}/> Comment</Button>
                  <Button variant="secondary"> <FontAwesomeIcon icon={faShare}/> Share</Button>
                </Card.Body>
            </Card>
          ))}
          </React.Fragment>
        )}
      </div>
    </PlurrPage>
  );
}

export default Stream;
