import React from 'react'
import './PostContent.css'
import { Row, Col, Image, Button, Card } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faHeart, faComment } from '@fortawesome/free-solid-svg-icons'
import { RiShareLine, RiShareFill } from 'react-icons/ri'
import { faHeart as farHeart, faComment as farComment } from '@fortawesome/free-regular-svg-icons'

export default function PostContent ({ author, post })  {
  
    return (
      <div>
        <Card key={1} className = 'Card my-5 border-0' style={{boxShadow: "#e0e3e8 0px 1px 1px, #e0e3e8 0px 1px 2px", borderRadius: "7px"}}>
          <Card.Body className="p-4">
            <Row>
              <Col xs={12} style={{display: 'flex', alignItems: 'center'}}>
                <a href={author.id} style={{textDecoration: "none"}}>
                <Image className='fluid' 
                  src={author?.profileImage} 
                  roundedCircle style={{objectFit: "cover", 
                    backgroundColor: "#EEE", width: "40px", height: "40px", marginRight: "8px"}} />
                  </a>
                <a href={author.id} style={{textDecoration: "none"}}>
                  <div style={{color: "#333", fontSize: "1rem", fontWeight: '700'}}>
                    {author.displayName}
                  </div>
                </a>
              </Col>
            </Row>
            <Card.Title className="mt-3" style={{fontSize: "1.2rem", fontWeight: '500'}}>
              {post.title}
            </Card.Title>
            <Card.Text className="mb-2">
                {post.content}
            </Card.Text>
            <Row>
              <Col xs={12} style={{display: 'flex', alignItems: 'center', gap: "10px"}}>
                <div className="icon-container like">
                    <FontAwesomeIcon 
                      style={{color:'grey', width: "18px", height: "18px"}} icon={farHeart}/>
                </div>
                <div className="icon-container comment">
                <FontAwesomeIcon
                  style={{color:'grey', width: "18px", height: "18px"}} icon={farComment}/>
                </div>
                <div className="icon-container share">
                  <RiShareLine style={{color:'grey', width: "18px", height: "18px"}} />
                </div>
              </Col>
            </Row>
          </Card.Body>
        </Card>
      </div>
    );
  }
  