import React, { useEffect, useState } from "react"
import Button from "react-bootstrap/esm/Button";
import Container from 'react-bootstrap/Container';
import Form from "react-bootstrap/Form";
import "./CreatePost.css";


export default function CreatePost() {


    return (
        <Container>
            <Form>
                <div class="form-group">
                    <label for="formGroupExampleInput">Example label</label>
                    <input type="text" class="form-control" id="formGroupExampleInput" placeholder="Example input" />
                </div>
                <div class="form-group">
                    <label for="formGroupExampleInput2">Another label</label>
                    <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Another input" />
                </div>
            </Form>
        </Container>
    );
}
