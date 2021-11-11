import React from "react";
import {Button, Modal, Form} from 'react-bootstrap';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { useUserHandler } from "../UserContext"
import * as Yup from 'yup';

export default function EditProfileModal({authorUUID, author, show, onHide, closeModal}) {

    const {setLoggedInUser} = useUserHandler()

    // schema to validate form inputs
    const validationSchema = Yup.object().shape({
      displayName: Yup.string().required('Full Name is required'),
      github: Yup.string().url()
        .required('Github link is required')
        .test("Valid Github Link", "GitHub link is invalid", (value) => {
            if (value) {
                return value.startsWith("https://github.com/");
            }
        })
    });

    // get form functions and link validation schema to form
    const { register, handleSubmit, formState: { errors } } = useForm({
      resolver: yupResolver(validationSchema)
    });

    const submitHandler = (data) => {
      fetch(`http://127.0.0.1:8000/service/author/${authorUUID}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(data)
      })
        .then((corsResponse) => {
          const apiPromise = corsResponse.text();
          apiPromise.then((apiResponse) => {
            const userData = JSON.parse(apiResponse).data
            const userObject = {
              ...JSON.parse(localStorage.getItem('user')), 
              displayName: userData.displayName, 
              github: userData.github
            }
            
            // set the logged in user
            localStorage.setItem('user', JSON.stringify(userObject));
            setLoggedInUser(userObject);

            closeModal();
          }).catch((error) => {
            console.log(error)
          })
        })
      };

    return (
      <Modal
        show={show}
        onHide={onHide}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            Edit your profile
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form onSubmit={handleSubmit(submitHandler)}>
            {/* displayName Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Full Name</Form.Label>
              <Form.Control defaultValue={author.displayName} name="displayName" placeholder="Full Name" 
                {...register('displayName')} 
                className={`form-control ${errors.displayName ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.displayName?.message}</Form.Text>
            </Form.Group>

            {/* github Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Github Link</Form.Label>
              <Form.Control defaultValue={author.github} name="github" placeholder="Github Link" 
                {...register('github')} 
                className={`form-control ${errors.github ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.github?.message}</Form.Text>
            </Form.Group>

            {/* Submit Button */}
            <div className="flex-row-reverse">
              <Button className="pl-5" variant="primary" type="submit">Save Changes</Button>
            </div>
          </Form>
       </Modal.Body>

      </Modal>
    );
  }
  