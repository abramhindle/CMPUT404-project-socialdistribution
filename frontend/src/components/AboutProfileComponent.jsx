import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import './styles/AboutProfileComponent.css';
import {Tab, Table, Button, Input, TextArea, Icon, Form, Message} from 'semantic-ui-react';
import PropTypes from 'prop-types';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import store from '../store/index.js';
import Cookies from 'js-cookie';
import AbortController from 'abort-controller';
import utils from "../util/utils";

const controller = new AbortController();
const signal = controller.signal;
signal.addEventListener("abort", () => {});

class AboutProfileComponent extends Component {

	constructor(props) {
		super(props);
		this.state = {
		    error: false,
            errorMessage: "",
            isEdit: false,
            profile_id: null,
            host: null,
            displayName: null,
            url: null,
            github: null,
            firstName: null,
            lastName: null,
            email: null,
            bio: null
        };

		this.handleChange = this.handleChange.bind(this);
		this.resetState = this.resetState.bind(this);
		this.getEditButton = this.getEditButton.bind(this);
	}

	onClickEditButton = () => {
	    this.resetState();
	    this.setState({
            isEdit: true
        });
    }

	componentDidUpdate() {
		if(this.state.isEdit) {
			this.scrollToBottom();
		}
	}

    componentWillUnmount() {
        controller.abort();
    }


	scrollToBottom() {
		this.element.scrollIntoView({ behavior: 'smooth' });
	}

    resetState() {
	    this.setState({
            error: false,
            errorMessage: "",
            isEdit: false,
            profile_id: null,
            host: null,
            displayName: null,
            url: null,
            github: null,
            firstName: null,
            lastName: null,
            email: null,
            bio: null
        });
    }

	onClickCancelButton = () => {
	    this.resetState();
    }

	onClickSaveButton = () => {
	    //call edit author endpoint
        const target = ["host", "displayName", "github", "firstName", "lastName", "email", "bio"],
            url = "/api/author/" + utils.getShortAuthorId(this.props.fullAuthorId);
        let requestBody = {};
        for (let i in target) {
            let key = target[i];
            if(this.state[key] !== null){
                requestBody[key] = this.state[key];
            }
        }
        HTTPFetchUtil.sendPostRequest(url, true, requestBody, signal)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.resetState();
                        this.setState({
                            isEdit: false,
                            error: false,
                            errorMessage: ""
                        });
                        //on success call on success prop
                        this.props.onSuccess()
                    });
                } else {
                    httpResponse.json().then((results) => {
                       this.setState({
                           error: true,
                           errorMessage: results
                        });
                    });
                };
            }).catch((error) => {
                console.error(error);
                this.setState({
                    error: true
                });
        });
    }

    handleChange(event) {
        this.setState({
            [event.target.name]: event.target.value
        });
    }

    getProfileCell = (name, value) => {
	    if(this.state.isEdit) {
	        return (
	            <Table.Cell>
                    <Input
                        name={name}
                        onChange={this.handleChange}
                        value={value}
                    />
                </Table.Cell>
            );
        };
	    if(value === "") {
	        value = "N/A"
        }
	    return (
            <Table.Cell>{value}</Table.Cell>
        );
    }

	getBioCell = (name, value) => {
	    if(this.state.isEdit) {
	        return (
	             <Table.Cell colSpan="2">
                    <Form>
                        <TextArea
                            rows={2}
                            name={name}
                            value={value}
                            onChange={this.handleChange}
                        />
                    </Form>
                </Table.Cell>
            );
        }
	    if(value === "") {
	        value = "N/A"
        }
	    return (
            <Table.Cell>{value}</Table.Cell>
        );
    }

	getEditButton() {
	    let currentFullUserId = store.getState().loginReducers.userId || Cookies.get("userID")
        if(currentFullUserId !== this.props.fullAuthorId) {
            return null;
        }

	    if(this.state.isEdit) {
	        return (
	            <div className="edit-button">
                <Button.Group>
                    <Button
                        onClick={this.onClickCancelButton}
                    >
                        Cancel
                    </Button>
                    <Button.Or />
                    <Button
                        positive
                        onClick={this.onClickSaveButton}
                    >
                        Save
                    </Button>
                </Button.Group>
                </div>
            );
        };
	    return (
	        <div className="edit-button">
                <Button icon labelPosition='left'
                    onClick={this.onClickEditButton}
                >
                  <Icon name='edit' />
                  Edit
                </Button>
            </div>
        );
    }

	getAboutPane() {
        return (
            <Tab.Pane>
                <Message negative hidden={!this.state.error}>
                    <Message.Header>Update Profile Failed</Message.Header>
                    <p>{this.state.errorMessage}</p>
                </Message>
                {this.getEditButton()}
                <Table basic>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell colSpan="2">Bio</Table.HeaderCell>
                            <Table.HeaderCell> </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            {this.getBioCell("bio", this.state.bio === null ? this.props.bio : this.state.bio)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Basic Information</Table.HeaderCell>
                            <Table.HeaderCell> </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Display Name</Table.HeaderCell>
                            {this.getProfileCell("displayName", this.state.displayName === null ? this.props.displayName : this.state.displayName)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>First Name</Table.HeaderCell>
                            {this.getProfileCell("firstName", this.state.firstName === null ? this.props.firstName : this.state.firstName)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Last Name</Table.HeaderCell>
                            {this.getProfileCell("lastName", this.state.lastName === null ? this.props.lastName : this.state.lastName)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Host</Table.HeaderCell>
                            <Table.Cell>{this.props.host}</Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Github</Table.HeaderCell>
                            {this.getProfileCell("github", this.state.github === null ? this.props.github : this.state.github)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Email</Table.HeaderCell>
                            {this.getProfileCell("email", this.state.email === null ? this.props.email : this.state.email)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>URL</Table.HeaderCell>
                            <Table.Cell>{this.props.url}</Table.Cell>
                        </Table.Row>
                    </Table.Header>
                </Table>
                <div ref={scrollToBottomReference => { this.element = scrollToBottomReference; }} />
            </Tab.Pane>
        );
    }

	render() {
        return(this.getAboutPane());
    }
}

AboutProfileComponent.propTypes = {
    fullAuthorId: PropTypes.string.isRequired,
	profile_id: PropTypes.string.isRequired,
	host: PropTypes.string.isRequired,
	displayName: PropTypes.string.isRequired,
	url: PropTypes.string.isRequired,
	github: PropTypes.string.isRequired,
	firstName: PropTypes.string.isRequired,
    lastName: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    bio: PropTypes.string.isRequired,
    onSuccess: PropTypes.func.isRequired
};

export default AboutProfileComponent;
