import React from 'react'
import { Row, Col, Image, Button } from 'react-bootstrap';
import EditProfileModal from '../components/EditProfileModal';


export default function Author ({ loggedInUser, author, authorFollowers })  {

  const showEdit = (author.id === loggedInUser.id);
  const [modalShowEdit, setModalShowEdit] = React.useState(false);

  return (    
    <div>
      <Row>
        <Col xs={6} md={10} style={{display: 'flex', alignItems: 'center'}}>
          <Image className='fluid' 
            src={author?.profileImage} 
            roundedCircle style={{objectFit: "cover", 
              backgroundColor: "#DDD", width: "50px", height: "50px", marginRight: "8px"}} />
          <div style={{color: "#333", fontSize: "1.3rem", fontWeight: '700'}}>{author.displayName}</div>
        </Col>
        <Col xs={6} md={2} style={{display: 'flex', alignItems: 'center'}}>
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
              (authorFollowers.items.filter(author => author.id === loggedInUser.id).length > 0) ? (
                <Button className="pl-5" variant="secondary" disabled style={{justifySelf: 'end'}}>Follow</Button>
              ) : (
                <Button className="pl-5" variant="outline-primary" style={{justifySelf: 'end'}}>Follow</Button>
              )
            )
          }
        </Col>
      </Row>
    </div>
  );
}
