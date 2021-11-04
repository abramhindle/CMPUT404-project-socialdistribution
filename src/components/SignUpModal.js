import React from "react";
import {Button, Modal, Form, InputGroup} from 'react-bootstrap';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEyeSlash, faEye } from '@fortawesome/free-solid-svg-icons';
import axios from "axios"
import * as Yup from 'yup';

export default function SignUpModal({show, onHide}) {
    // boolean for showing or hiding the password
    const [passwordHidden, setPasswordHidden] = React.useState(true);

    // schema to validate form inputs
    const validationSchema = Yup.object().shape({
      username: Yup.string()
        .required('Username is required')
        .min(6, 'Username must be at least 6 characters')
        .max(20, 'Username must not exceed 20 characters'),
      password: Yup.string()
        .required('Password is required')
        .min(8, 'Password must be at least 8 characters')
        .max(40, 'Password must not exceed 40 characters'),
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
    const { register, handleSubmit, reset, setError, formState: { errors } } = useForm({
      resolver: yupResolver(validationSchema)
    });

    const submitHandler = (data) => {
      // post the validated data to the backend registration service
      axios
        .post("http://127.0.0.1:8000/service/author/register/", data)
        .then(() => {
          // empty out the form
          reset();
          
          // alert the user that their account creation was successful
          alert("Your account has been created. " + 
            "You'll be able to log in when it is activated!")
        })
        .catch((e) => {
          // get the errors object
          const errors = e.response.data;

          // set username errors
          if (errors.username) {
            setError('username', {
              type: "server",
              message: errors.username[0],
            });
          }

          // set password errors
          if (errors.password) {
            setError('password', {
              type: "server",
              message: errors.password[0],
            });
          }

          // set displayName errors
          if (errors.displayName) {
            setError('displayName', {
              type: "server",
              message: errors.displayName[0],
            });
          }

          // set github errors
          if (errors.github) {
            setError('github', {
              type: "server",
              message: errors.github[0],
            });
          }
        });
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
            Create your account
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form onSubmit={handleSubmit(submitHandler)}>
            {/* username Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Username</Form.Label>
              <Form.Control defaultValue="" name="username" placeholder="Username" 
                {...register('username')} 
                className={`form-control ${errors.username ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.username?.message}</Form.Text>
            </Form.Group>

            {/* password Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Password</Form.Label>
              <InputGroup>
              <Form.Control defaultValue="" name="password" 
                type={passwordHidden ? "password" : "text"} placeholder="Password" 
                {...register('password')} 
                className={`form-control ${errors.password ? 'is-invalid' : ''}`}/>
                  <InputGroup.Text style={{"cursor": "pointer"}} 
                    onClick={() => {setPasswordHidden(!passwordHidden)}}>
                      <FontAwesomeIcon icon={passwordHidden ? faEyeSlash : faEye}/>
                  </InputGroup.Text>
              <Form.Text className="invalid-feedback">{errors.password?.message}</Form.Text>
              </InputGroup>
            </Form.Group>

            {/* displayName Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Full Name</Form.Label>
              <Form.Control defaultValue="" name="displayName" placeholder="Full Name" 
                {...register('displayName')} 
                className={`form-control ${errors.displayName ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.displayName?.message}</Form.Text>
            </Form.Group>

            {/* github Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Github Link</Form.Label>
              <Form.Control defaultValue="" name="github" placeholder="Github Link" 
                {...register('github')} 
                className={`form-control ${errors.github ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.github?.message}</Form.Text>
            </Form.Group>

            {/* Submit Button */}
            <div className="flex-row-reverse">
              <Button className="pl-5" variant="primary" type="submit" >Sign Up</Button>
            </div>
          </Form>
       </Modal.Body>

      </Modal>
    );
  }
  