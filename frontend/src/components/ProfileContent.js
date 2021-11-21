import React, { useState, useEffect } from "react";
import { Row, Col, Button, Image, Alert } from "react-bootstrap";
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import { LinkContainer } from "react-router-bootstrap";

import Message from "../components/Message";
import { getAuthorDetail, getUsers } from "../actions/userActions";
import { useDispatch, useSelector } from "react-redux";
import jQuery from "jquery";

function ProfileContent(props) {
  // update this page when view correctly returns author detail

  const dispatch = useDispatch();

  const userDetail = useSelector((state) => state.userDetail);
  const { error, loading, userInfo } = userDetail;

  // currently just returns logged in user's info;
  // later, fix page url to reflect different author's profile and get info by passing their id.
  useEffect(() => {
    if (userInfo == null) {
      dispatch(getAuthorDetail());
    }
  }, [dispatch, userInfo]);

  console.log(userDetail);

  const view_user_id = props.view_user_id;
  console.log(view_user_id);


  const userList = useSelector((state) => state.userList);
  //const { error, loading1, userList } = userList;
  const userList1 = null;
  useEffect(() => {
    if (userList1 == null) {
      dispatch(getUsers());
    }
  }, [dispatch, userList1]);

  // console.log("heere");
  // console.log(userList1);
  // console.log("end");
  // get null


  return (
    <div className="m-5">

      <Button 
        className="m-1" style={{width:"auto"}} variant={'success'}>
        {view_user_id ? 'I\'m viewing '+view_user_id+'\'s profile' : 'My profile page'}
      </Button>
      <Row className="justify-content-between">
        
        <Col md={8}>
          <Row className="justify-content-between">
            <Col md={6}>
              <Image src={Avatar} width="100%" className="mb-5" />
            </Col>
            <Col md={2} className="d-flex flex-column mt-auto">
              <LinkContainer
                to="/editprofile"
                className="p-2 my-5"
                style={{ backgroundColor: "orange" }}
              >
                {/* visible if it's ur own profile */}
                <Button>
                  <Image src={EditIcon} width="50%" />
                </Button>
              </LinkContainer>
            </Col>
          </Row>
          <Alert>
            Display Name:&#160;&#160;
            <h5 className="d-inline">{userInfo ? userInfo.displayName : ""}</h5>
          </Alert>
          <Alert>
            Github:&#160;&#160;
            <h5 className="d-inline">{userInfo ? userInfo.github : ""}</h5>
          </Alert>
        </Col>
        {/* show or hide request buttons*/}
        {view_user_id ?
        <Col md={2}>
          {/* neither following */}
          <Button className="m-2">Add Friend</Button>
          {/* visibile when following or friends */}
          <Button className="m-2" variant="success">
            Following
          </Button>
          <Button className="m-2" variant="danger">
            Unfollow
          </Button>
          {/* visibile when incoming friend request */}
          <Button className="m-2" variant="success">
            Accept Friend Request
          </Button>
          <Button className="m-2" variant="danger">
            Decline Friend Request
          </Button>
        </Col> : null}
      </Row>
    </div>
  );
}

export default ProfileContent;
