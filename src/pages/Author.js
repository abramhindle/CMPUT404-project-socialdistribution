import React from 'react'
import { Row, Col, Image, Button } from 'react-bootstrap';
import EditProfileModal from '../components/EditProfileModal';
import PostContent from '../components/PostContent';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGithub } from "@fortawesome/free-brands-svg-icons"


export default function Author ({ loggedInUser, author, authorFollowers, posts })  {

  const showEdit = (author.id === loggedInUser.id);
  const [modalShowEdit, setModalShowEdit] = React.useState(false);

  return (    
    <div>
      <Row>
        <Col xs={6} md={10} style={{display: 'flex', alignItems: 'center'}}>
          <Image className='fluid' 
            src={author?.profileImage} 
            roundedCircle style={{objectFit: "cover", 
              backgroundColor: "#EEE", width: "50px", height: "50px", marginRight: "12px"}} />
          <div style={{color: "#333", fontSize: "1.3rem", fontWeight: '700', marginRight: "7px"}}>{author.displayName}</div>
          <a href={author.github}>
            <FontAwesomeIcon icon={faGithub} style={{width: "23px", height: "23px", marginTop: "0px", color: "#777"}}/>
          </a>
        </Col>
        <Col xs={6} md={2} style={{display: 'flex', alignItems: 'center', justifyContent: 'end'}}>
          {
            showEdit ? (
              <>
                <Button className="pl-5" variant="outline-primary" 
                  style={{justifySelf: 'end', padding: "5px 20px"}}
                  onClick={() => setModalShowEdit(true)}>Edit</Button>
                <EditProfileModal
                  authorUUID={loggedInUser.uuid}
                  author={author}
                  show={modalShowEdit}
                  onHide={() => setModalShowEdit(false)}
                  closeModal={() => setModalShowEdit(false)}
                />
              </>
            ) : (
              (authorFollowers?.items?.filter(author => author.id === loggedInUser.id).length > 0) ? (
                <Button className="pl-5" variant="secondary" disabled>Follow</Button>
              ) : (
                <Button className="pl-5" variant="outline-primary">Follow</Button>
              )
            )
          }
        </Col>
      </Row>
      { posts && posts.items?.map((post) => {
          return <PostContent key={post.id} author={author} post={post} />
        })
      }
    </div>
  );
}
