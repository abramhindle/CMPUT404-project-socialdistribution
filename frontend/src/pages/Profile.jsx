import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import SideBar from '../components/SideBar';
import ProfileBubble from '../components/ProfileBubble';
import './styles/Profile.css'
import { Container } from 'semantic-ui-react'
import { Tab } from 'semantic-ui-react'
import { Table } from 'semantic-ui-react'

class Profile extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
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
                            Hi, I am Henry Truong! I am a senior developer.
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
                            <Table.Cell>Henry Truong</Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Github</Table.Cell>
                            <Table.Cell><a href="https://github.com/htruong1">https://github.com/htruong1</a></Table.Cell>
                        </Table.Row>
                        <Table.Row>
                            <Table.Cell>Email</Table.Cell>
                            <Table.Cell><a href="mailto:truong@raiseyourtruongers.com">htruong1@email.com</a></Table.Cell>
                        </Table.Row>
                        </Table.Body>
                    </Table>
                </Tab.Pane> },
                { menuItem: 'Posts', render: () => <Tab.Pane>Stream component goes here</Tab.Pane> },
                { menuItem: 'Friends', render: () => <Tab.Pane>Friend List component goes here</Tab.Pane> },
              ]
        )
    }

	render() {
	return(
		    <Container>
                <SideBar/>
                    <div className="profile">
                        <ProfileBubble
                        profileBubbleClassAttributes={"ui centered top aligned circular bordered small image"}/>
                        <br/><div className="profile-username">htruong1</div>
                            <button class="positive ui button">
                            <i class="user plus icon"></i>
                            Request Friend
                            </button>
                    
                    <div>
                        <Tab panes={this.showPanes()}></Tab>
                    </div>
                    </div>
            </Container>
	    )
    }
}

export default Profile;
