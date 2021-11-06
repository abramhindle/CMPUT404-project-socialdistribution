import React from 'react'
import './Authors.css'
import { Button, Card } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeart, faComment, faShare } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from "@fortawesome/free-brands-svg-icons"

function Authors ({ authors })  {
    const [isLiked, setLiked] = React.useState(false);

    function toggleLiked() {
      setLiked(!isLiked)  
    };
  
    return (
      <div>
        <h1 className='Authors-leftColLink' style={{color: "black"}}> 
          My Plurr Authors
        </h1>
        {authors?.items?.map((author, count) => (  
          <Card key={count} className = 'Card my-5'>
            <Card.Img variant="top" src={author.profileImage}/>
            <Card.Body>
              <Card.Title>
                <a href={author.id}>@{author.displayName}</a>
                <a href={author.github}>
                  <FontAwesomeIcon icon={faGithub}/>
                </a>
              </Card.Title>
              <Card.Text>
                  {author.profileImage}
                  {author.github}
              </Card.Text>
                <Button onClick={() => toggleLiked()} variant="danger">
                  <FontAwesomeIcon 
                    style={ isLiked ?{color:'black'} : null} icon={faHeart}/>
                  &nbsp;{isLiked? 'Liked' : 'Like'}
                </Button>
              <Button variant="primary"> 
                <FontAwesomeIcon icon={faComment}/> Comment
              </Button>
              <Button variant="secondary"> 
                <FontAwesomeIcon icon={faShare}/> Share
              </Button>
            </Card.Body>
          </Card>
        ))}
      </div>
    );
  }
  
  export default Authors;
  
  
  