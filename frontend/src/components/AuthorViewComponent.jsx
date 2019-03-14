import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import ProfileBubble from './ProfileBubble';
import './styles/AuthorViewComponent.css';
import { Container, Tab, Table } from 'semantic-ui-react';

class AuthorViewComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {
            bio: "bio"
		}
	}

    tabPanes = [
                { menuItem: 'About', render: () => 
                <Tab.Pane>
                    <Table basic>
                        {/* <Table.Header>
                            <Table.Row>{this.props.bio}</Table.Row>
                            <Table.Row>{this.props.displayName}</Table.Row>
                        </Table.Header>  */}
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell>Bio</Table.HeaderCell>
                                <Table.HeaderCell> </Table.HeaderCell>
                            </Table.Row>
                            <Table.Row>
                                <Table.Cell>{this.props.data.displayName}</Table.Cell>
                                <Table.Cell> </Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.HeaderCell>Basic Information</Table.HeaderCell>
                                <Table.HeaderCell> </Table.HeaderCell>
                            </Table.Row>
                            <Table.Row>
                                <Table.HeaderCell>Github</Table.HeaderCell>
                                <Table.Cell>{this.props.data.github}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.HeaderCell>Email</Table.HeaderCell>
                                <Table.Cell>{this.props.data.email}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.HeaderCell>Name</Table.HeaderCell>
                                <Table.Cell>{this.props.data.firstName+" "+this.props.data.lastName}</Table.Cell>
                            </Table.Row>
                            <Table.Row>
                                <Table.HeaderCell>URL</Table.HeaderCell>
                                <Table.Cell>{this.props.data.id}</Table.Cell>
                            </Table.Row>
                        </Table.Header>
                    </Table>
                </Tab.Pane>},
                { menuItem: 'Posts', render: () => <Tab.Pane>Stream component goes here</Tab.Pane> },
                { menuItem: 'Friends', render: () => <Tab.Pane>Friend List component goes here</Tab.Pane> },
              ]

	render() {
        return(
                <div className="profile">
                    <ProfileBubble profileBubbleClassAttributes={"ui centered top aligned circular bordered small image"}/>
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

export default AuthorViewComponent;
