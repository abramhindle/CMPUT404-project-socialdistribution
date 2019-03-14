import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import SideBar from '../components/SideBar';
import FriendListComponent from '../components/FriendsListComponent';
import ProfileBubble from '../components/ProfileBubble';
import './styles/Profile.css';
import { Container } from 'semantic-ui-react';
import { Tab } from 'semantic-ui-react';
import { Table } from 'semantic-ui-react';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';
import store from "../store/index";

class Profile extends Component {	

	constructor(props) {
        super(props);
		this.state = {
            profiledata: []
        };
        this.getProfile = this.getProfile.bind(this);
        this.showPanes = this.showPanes.bind(this);
    }

    showPanes = () => {
        return (
            [
                { menuItem: 'About', render: () => <Tab.Pane>
                    <Table basic='very'>
                    <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Bio</Table.HeaderCell>
                            <Table.HeaderCell></Table.HeaderCell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>{this.state.profiledata.bio}</Table.Cell>
                        </Table.Row>
                    </Table.Header>
                    </Table>

                    <Table basic='very'>    
                        <Table.Header>
                        <Table.Row>
                            <Table.HeaderCell>Basic Information</Table.HeaderCell>
                            <Table.HeaderCell></Table.HeaderCell>
                        </Table.Row>
                        </Table.Header>

                        <Table.Body>
                        <Table.Row>
                            <Table.Cell>Name</Table.Cell>
                            <Table.Cell>{this.state.profiledata.firstName} {this.state.profiledata.lastName}</Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Github</Table.Cell>
                            <Table.Cell><a href={this.state.profiledata.github} target="_blank" rel="noopener noreferrer">{this.state.profiledata.github}</a>
                            </Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Email</Table.Cell>
                            <Table.Cell>{this.state.profiledata.email}
                            </Table.Cell>
                        </Table.Row>
                        </Table.Body>
                    </Table>
                </Tab.Pane> },
                { menuItem: 'Posts', render: () => <Tab.Pane>Stream component goes here</Tab.Pane> },
                { menuItem: 'Friends', render: () => <Tab.Pane><FriendListComponent/></Tab.Pane> },
              ]
        )
    }

    componentDidMount() {
        this.getProfile();
    }

    getProfile() {
        var urlPath = "/api/author/"
        var authorId = store.getState().loginReducers.userId.split("author/");
        const path = urlPath + authorId[1], requireAuth = true;
        HTTPFetchUtil.getRequest(path, requireAuth)
        .then((httpResponse) => {
            if (httpResponse.status === 200) {
                httpResponse.json().then((results) => {
                    this.setState( {
                        profiledata: results
                    })
                })
                .catch((error) => {
                    console.log(error);
                });
            }
            else {
                alert("HTTPRequest error");
                console.log(httpResponse);
            }
        })
    }

	render() {
	    return(
		    <Container>
                <SideBar/>
                    <div className="profile">
                        <br/>
                        <ProfileBubble
                        profileBubbleClassAttributes={"ui centered top aligned circular bordered small image"} profilePicture={null} username = {this.state.username}/>
                        <br/><div className="profile-username">{this.state.profiledata.displayName}</div>
                    <div>
                        <Tab panes={this.showPanes()}></Tab>
                    </div>
                    </div>
            </Container>
	    )
    }
}

export default Profile;