import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import ProfileBubble from './ProfileBubble';
import './styles/AuthorViewComponent.css';
import {Tab, Table, Button, Input, TextArea, Icon, Form, Message} from 'semantic-ui-react';
import PropTypes from 'prop-types';
import HTTPFetchUtil from "../util/HTTPFetchUtil";

class AuthorViewComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
            isEdit: false
		};
		this.handleChange = this.handleChange.bind(this);
	}

	onClickEditButton = () => {
	    let current = this.state.isEdit;
	    this.setState({
            isEdit: !current
        });
    };

	onClickCancelButton = () => {
	    let current = this.state.isEdit;
	    this.setState({
            error: false,
            errorMessage: "",
            isEdit: !current,
            profile_id: "",
            host: "",
            displayName: "",
            url: "",
            github: "",
            firstName: "",
            lastName: "",
            email: "",
            bio: ""
        });
    };

	onClickSaveButton = () => {
	    //call edit author endpoint
        const requestBody = {
            displayName: this.state.displayName,
            github: this.state.github,
            firstName: this.state.firstName,
            lastName: this.state.lastName,
            email: this.state.email,
            bio: this.state.bio
        },
        url = "/api/author/" + "df57cce0-8eae-44d9-8f43-8033e099b917";
        console.log(this.props)
        HTTPFetchUtil.sendPostRequest(this.props.hostURL, true, requestBody)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        let current = this.state.isEdit;
                        this.setState({
                            isEdit: !current
                        });
                        //on success call on success prop
                        this.props.onSuccess()
                    })
                } else {
                    httpResponse.json().then((results) => {
                       this.setState({
                           error: true,
                           errorMessage: results
                        });
                    });
                }
            })
            .catch((error) => {
                console.error(error);
                this.setState({
                    error: true
                });
        });


    };

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
        }
	    return (
            <Table.Cell>{value}</Table.Cell>
        );
    };

	getNameCell = () => {
	    if(this.state.isEdit) {
	        return (
	            <Table.Cell>
                    <Input
                        name="firstName"
                        value={this.state.firstName || this.props.firstName}
                        onChange={this.handleChange}
                    />
                    <Input
                        name="lastName"
                        value={this.state.lastName || this.props.lastName}
                        onChange={this.handleChange}
                    />
                </Table.Cell>
            );
        }
	    return (
            <Table.Cell>{this.props.firstName+" "+this.props.lastName}</Table.Cell>
        );
    };

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
	    return (
            <Table.Cell>{value}</Table.Cell>
        );
    };

	getButton() {
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
        }
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
                {this.getButton()}
                <Table basic>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell colSpan="2">Bio</Table.HeaderCell>
                            <Table.HeaderCell> </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            {this.getBioCell("bio", this.state.bio || this.props.bio)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Basic Information</Table.HeaderCell>
                            <Table.HeaderCell> </Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Display Name</Table.HeaderCell>
                            {this.getProfileCell("displayName", this.state.displayName || this.props.displayName)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Name</Table.HeaderCell>
                            {this.getNameCell()}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Host</Table.HeaderCell>
                            <Table.Cell>{this.props.host}</Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Github</Table.HeaderCell>
                            {this.getProfileCell("github", this.state.github || this.props.github)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>Email</Table.HeaderCell>
                            {this.getProfileCell("email", this.state.email || this.props.email)}
                        </Table.Row>
                        <Table.Row>
                            <Table.HeaderCell>URL</Table.HeaderCell>
                            <Table.Cell>{this.props.url}</Table.Cell>
                        </Table.Row>
                    </Table.Header>
                </Table>
            </Tab.Pane>
        );
    }

    getPostsPane() {
	    return (
	        <Tab.Pane>Stream component goes here</Tab.Pane>
        );
    }

    getFriendsPane() {
	    return (
	        <Tab.Pane>Friend List component goes here</Tab.Pane>
        );
    }

    tabPanes = [
                { menuItem: 'About', render: () => this.getAboutPane()},
                { menuItem: 'Posts', render: () => this.getPostsPane()},
                { menuItem: 'Friends', render: () =>  this.getFriendsPane()},
              ]

	render() {
        return(
                <div className="profile">
                    <ProfileBubble
                        username={this.props.displayName}
                        profileBubbleClassAttributes={"ui centered top aligned circular bordered small image"}
                    />
                    <br/>
                    <div className="profile-username">
                        htruong1
                    </div>
                    <button id="addAuthorButton" className="positive ui button">
                        <i className="user plus icon"></i>
                        Request Friend
                    </button>
                    <div>
                        <Tab panes={this.tabPanes}></Tab>
                    </div>
                </div>
            )
    }
}

AuthorViewComponent.propTypes = {
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

export default AuthorViewComponent;
