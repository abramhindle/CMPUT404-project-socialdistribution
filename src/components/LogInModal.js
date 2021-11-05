import React from "react";
import {Button, Modal, Form, InputGroup} from 'react-bootstrap';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEyeSlash, faEye } from '@fortawesome/free-solid-svg-icons';
import { useUserHandler } from "../UserContext"
import { useHistory } from "react-router-dom"
import axios from "axios"
import * as Yup from 'yup';

export default function LogInModal({show, onHide, closeModal}) {
    // boolean for showing or hiding the password
    const [passwordHidden, setPasswordHidden] = React.useState(true);
    const [invalidCredentials, setInvalidCredentials] = React.useState(false);
    const {setLoggedInUser} = useUserHandler()

    // redirect away from the Login modal with useHistory
    const history = useHistory()

    // schema to validate form inputs
    const validationSchema = Yup.object().shape({
      username: Yup.string()
        .required('Username is required'),
      password: Yup.string()
        .required('Password is required')
    });

    // get form functions and link validation schema to form
    const { register, handleSubmit, reset, setError, formState: { errors } } = useForm({
      resolver: yupResolver(validationSchema)
    });

    const submitHandler = (data) => {
      // remove invalid credentials error
      setInvalidCredentials(false)

      // post the validated data to the backend registration service
      axios
        .post("http://127.0.0.1:8000/service/author/login/", data)
        .then((response) => {  
          // close the modal
          closeModal();

          // empty out the form
          reset();
          
          // reset the token
          localStorage.removeItem("token");
          localStorage.removeItem("user");
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('user', JSON.stringify({...response.data.user}));
          
          // set the logged in user
          setLoggedInUser({...response.data.user});

          history.push(`/stream`)
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

          // show invalid credentials error
          setInvalidCredentials(true)

          // clear any existing tokens
          localStorage.removeItem("token");
          localStorage.removeItem("user");
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
            Log in to Plurr
          </Modal.Title>
        </Modal.Header>

        {/* show error when credentials are invalid */}
        {invalidCredentials ? 
          <div className="alert alert-danger mb-0 rounded-0 alert-dismissible fade show">
            <strong>Error!</strong>&nbsp; Invalid credentials. Your account may not have been activated yet.
          </div> 
          : null
        }

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

            {/* Submit Button */}
            <div className="flex-row-reverse">
              <Button className="pl-5" variant="primary" type="submit" >Log In</Button>
            </div>
          </Form>
       </Modal.Body>

      </Modal>
    );
  }
  