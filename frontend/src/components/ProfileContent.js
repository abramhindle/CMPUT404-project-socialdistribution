import React, { useState, useEffect } from "react";
import { Row, Col, Button, Image, Alert } from "react-bootstrap";
import Avatar from "../images/avatar.jpg";
import EditIcon from "../images/edit.png";
import { LinkContainer } from "react-router-bootstrap";

import Message from "../components/Message";
import { getAuthorDetail } from "../actions/userActions";
import { useDispatch, useSelector } from "react-redux";
import jQuery from "jquery";

function ProfileContent() {
  // update this page when view correctly returns author detail

  const dispatch = useDispatch();

  const userDetail = useSelector((state) => state.userDetail);
  const { error, loading, userInfo } = userDetail;

  // reference: https://stackoverflow.com/a/50735730
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie("csrftoken");

  useEffect(() => {
    console.log(csrftoken);
    dispatch(getAuthorDetail(csrftoken));
  }, [dispatch, csrftoken, userInfo]);

  return (
    <div className="m-5">
      <Row className="justify-content-between">
        <Col md={8}>
          <Row className="justify-content-between">
            <Col md={6}>
              <Image src={Avatar} width="100%" className="mb-5" />
            </Col>
            <Col md={2} className="d-flex flex-column mt-auto">
              <LinkContainer
                to="/changeprofile"
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
          <Alert>Display Name: </Alert>
          <Alert>Github: </Alert>
        </Col>
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
        </Col>
      </Row>
    </div>
  );
}

export default ProfileContent;
