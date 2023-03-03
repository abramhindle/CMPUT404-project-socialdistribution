import React, { useState } from "react";
import Container from 'react-bootstrap/Container';
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import "./Signup.css";


// https://sst.dev/chapters/create-a-login-page.html

export default function Signup() {
    " State variables, stores the user inputs"
    const [email, setEmail] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    function validateForm() {
        return email.length > 0 && password.length > 0;
    }

    function handleSubmit(event) {
        event.preventDefault();
    }

    return (
        <Container>

            <Form className="Login">
                <img className="Logo" src="" alt=""/>
                <h1>Sign Up</h1>
                <Form.Group size="lg" controlId="email">
                <Form.Label>Email</Form.Label>
                <Form.Control
                    autoFocus
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                </Form.Group>
                <Form.Group size="lg" controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                </Form.Group>
                <Form.Group size="lg" controlId="password">
                <Form.Label>Confirm Password</Form.Label>
                <Form.Control
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                </Form.Group>
                <Button block="true" size="lg" type="submit" disabled={!validateForm()}>
                    Submit
                </Button>
            </Form>
        </Container>
      );
}