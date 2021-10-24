import Button from "@restart/ui/esm/Button";
import { style } from "dom-helpers";
import React from "react";
import { ButtonGroup, Form, Stack } from "react-bootstrap";
import { Link } from "react-router-dom";
import Headers from "../components/Headers";



function LoginPage() {
  return (
    <Stack>
      <Headers></Headers>
      <Stack style={{marginTop:100}}>
        <Form style={{marginLeft:550}}>
          <Form.Group className="mb-3" controlId="formBasicUsername">
          <Form.Label style={{color:"orange"}}>Username</Form.Label>
          <Form.Control style={{width:300}} type="username" placeholder=""></Form.Control>
          </Form.Group>
        </Form>
        <Form style={{marginLeft:550}}>
          <Form.Group className="mb-3" controlId="formBasicEmail">
          <Form.Label style={{color:"orange"}}>Password</Form.Label>
          <Form.Control style={{width:300}}type="password" placeholder=""></Form.Control>
          </Form.Group>
        </Form>
        <ButtonGroup>
          <a href="/">
              <Button style={{marginLeft:560, backgroundColor:"black", color:"white"}}>Login</Button>
          </a>
          <a href="/signup">
              <Button style={{marginLeft:40, color:"white", backgroundColor:"orange"}}>Create a new account</Button>
          </a>
        </ButtonGroup>
      </Stack>

    </Stack>
  );
}

export default LoginPage;
