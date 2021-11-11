import React from 'react'
import { Button, Card} from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeart, faComment, faShare } from '@fortawesome/free-solid-svg-icons'
import { faGithub } from "@fortawesome/free-brands-svg-icons"


function Inbox ({ authors })  {
  const [isLiked, setLiked] = React.useState(false);

  function toggleLiked() {
    setLiked(!isLiked)  
  };
  
  return (
    <div>
      <h1 className='' style={{color: "black"}}> My Plurr Feed</h1>
      {authors?.items?.map((author, count) => (   
        <Card key={count} className='Card my-5' style={{width: "100%"}}>
          {/* <Card.Img variant="top" 
            src="https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png" /> 
          */}
          <Card.Body>
            <Card.Title>
              <a href={author.id}>@{author.displayName}</a>
              <a href={author.github}>
                <FontAwesomeIcon icon={faGithub}/>
              </a>
            </Card.Title>
            {/* <Card.Subtitle className="mb-2 text-muted">{author.type}
              </Card.Subtitle> */}
            <Card.Text>
              Example post, a picture of a cat, by a dog
            </Card.Text>
            <Button onClick={() => toggleLiked(2)} variant="danger">
              <FontAwesomeIcon style={ isLiked ?{color:'black'} : null} icon={faHeart}/> 
              {isLiked? 'Liked' : 'Like'}
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

export default Inbox;
