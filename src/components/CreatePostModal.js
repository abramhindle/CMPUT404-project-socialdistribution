import React from "react";
import {Button, Modal, Form, InputGroup} from 'react-bootstrap';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEyeSlash, faEye } from '@fortawesome/free-solid-svg-icons';
import axios from "axios"
import * as Yup from 'yup';

export default function CreatePostModal({show, onHide, closeModal}) {
    // schema to validate form inputs
    const validationSchema = Yup.object().shape({
      title: Yup.string()
        .required('Title is required'),
      description: Yup.string()
        .required('Description is required'),
    visibility: Yup.string().required('Visibility is required'),
      type: Yup.string()
    });

    // get host (e.g. "https://plurr.herokuapp.com/")
    const getHost = () => {
      return ((window !== null) && (window !== undefined)) 
        ? window.location.href.split("/").slice(0, 4).join("/") : null
    }

    // get form functions and link validation schema to form
    const { register, handleSubmit, reset, setError, formState: { errors } } = useForm({
      resolver: yupResolver(validationSchema)
    });

    const submitHandler = (data) => {
      // get the host
      const host = getHost()

      // post the validated data to the backend registration service
      axios
      ///////// I"M AWARE THAT THE AUTHOR_ID NEEDS TO HAVE THE CORRECT AUTHOR THAT IS LOGGED IN /////////
        .post("http://127.0.0.1:8000/service/author/{AUTHOR_ID}/posts/", 
          (host === null) ? data : {...data, host})
        .then(() => {
          // close the modal
          closeModal();
          // empty out the form
          reset();
          
          setTimeout(() => {
            // alert the user that their post has been published 
            alert("Your post has been created. " + 
              "You'll be able to see your post publised")
          }, 500)
        })
        .catch((e) => {
          // get the errors object
          const errors = e.response.data;

          // set title errors
          if (errors.title) {
            setError('title', {
              type: "server",
              message: errors.title[0],
            });
          }

          // set description errors
          if (errors.description) {
            setError('description', {
              type: "server",
              message: errors.description[0],
            });
          }

          // set visibility errors
          if (errors.visibility) {
            setError('visibility', {
              type: "server",
              message: errors.visibility[0],
            });
          }

          // set type errors
          if (errors.type) {
            setError('type', {
              type: "server",
              message: errors.type[0],
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
            Create a post
          </Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <Form onSubmit={handleSubmit(submitHandler)}>
            {/* Title Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Title</Form.Label>
              <Form.Control defaultValue="" name="title" placeholder="Title" 
                {...register('title')} 
                className={`form-control ${errors.title ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.title?.message}</Form.Text>
            </Form.Group>

            {/* Description Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Description</Form.Label>
              <Form.Control defaultValue="" name="description" placeholder="Description" 
                {...register('description')} 
                className={`form-control ${errors.description ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.description?.message}</Form.Text>
            </Form.Group>

            {/* Visibility Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Visibility</Form.Label>
              <Form.Control defaultValue="" name="visibility" placeholder="Visibility" 
                {...register('visibility')} 
                className={`form-control ${errors.visibility ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.visibility?.message}</Form.Text>
            </Form.Group>

            {/* Type Form Field */}
            <Form.Group className="mb-3">
              <Form.Label>Type</Form.Label>
              <Form.Control defaultValue="" name="type" placeholder="Type" 
                {...register('type')} 
                className={`form-control ${errors.type ? 'is-invalid' : ''}`}/>
              <Form.Text className="invalid-feedback">{errors.type?.message}</Form.Text>
            </Form.Group>

            {/* Submit Button */}
            <div className="flex-row-reverse">
              <Button className="pl-5" variant="primary" type="submit" >Post</Button>
            </div>
          </Form>
       </Modal.Body>

      </Modal>
    );
  }
  