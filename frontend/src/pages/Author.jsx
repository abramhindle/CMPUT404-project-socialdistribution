import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import {Tab, Button, Icon} from "semantic-ui-react";
import ProfileBubble from "../components/ProfileBubble";
import StreamFeed from '../components/StreamFeed';
import AboutProfileComponent from "../components/AboutProfileComponent";
import './styles/Author.css';
import utils from "../util/utils";
import { SemanticToastContainer, toast } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';
import store from "../store/index";


class Author extends Component {

    constructor(props) {
		super(props);
		this.state = {
            isEdit: false,
            isSelf: false,
            isFollowing: false,
            bio: "",
            displayName: "",
            email: "",
            firstName: "",
            github: "",
            host: "",
            id: "",
            url: "",
            lastName: "",
		};
        this.fetchProfile = this.fetchProfile.bind(this);
        this.sendFollowRequest = this.sendFollowRequest.bind(this);
        this.getFollowButton = this.getFollowButton.bind(this);
        this.sendUnfollowRequest = this.sendUnfollowRequest.bind(this);
	}

	fetchProfile() {
        //todo deal with other hosts
        const hostUrl = "/api/author/"+ utils.getShortAuthorId(this.props.location.state.fullAuthorId),
            requireAuth = true;
        HTTPFetchUtil.getRequest(hostUrl, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.setState({
                            bio: results.bio,
                            displayName: results.displayName,
                            email: results.email,
                            firstName: results.firstName,
                            github: results.github,
                            host: results.host,
                            id: results.id,
                            url: results.url,
                            lastName: results.lastName,
                            isSelf: results.id === store.getState().loginReducers.userId,
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }

    getFollowButton() {
        let followbutton;
        if (this.state.isSelf) {
            return null;
        }

        else if (!this.state.isFollowing) {
            followbutton = <Button positive onClick={this.sendFollowRequest}><Icon name = "user plus" />Follow</Button>
        }

        else if (this.state.isFollowing) {
            followbutton = <Button negative onClick={this.sendUnfollowRequest}><Icon name = "user times"/>Unfollow</Button>
        }

        return <div>{followbutton}</div>;
    
    }

    sendUnfollowRequest() {
        let urlPath = "/api/unfollow/"
		let body = {
			query: "unfollow",
			author: {
				id: store.getState().loginReducers.userId,
				host: store.getState().loginReducers.hostName,
			},
			friend:{
				id: this.props.location.state.fullAuthorId,
				host: this.props.location.state.host,
			}
		}
		HTTPFetchUtil.sendPostRequest(urlPath, true, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.setState({
                            isFollowing: false
                        })
						toast(
							{
								type: 'success',
								icon: 'user',
								title: 'Unfollow successful!',
								description: <p>You are now following {this.props.location.state.displayName}</p>
							}
						);

                    })
				}
				else{
					console.log(httpResponse)
					toast(
						{
							type: 'error',
							icon: 'warning',
							title: 'Error: User could not be unfollowed!'
						}
					);
				}
            })
            .catch((error) => {
                console.error(error);
        });
    }

    sendFollowRequest() {
		let urlPath = "/api/friendrequest/"
		let body = {
			query: "friendrequest",
			author: {
				id: store.getState().loginReducers.userId,
				host: store.getState().loginReducers.hostName,
			},
			friend:{
				id: this.props.location.state.fullAuthorId,
				host: this.props.location.state.host,
			}
		}
		HTTPFetchUtil.sendPostRequest(urlPath, true, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.setState({
                            isFollowing: true
                        })
						toast(
							{
								type: 'success',
								icon: 'user',
								title: 'Follow successful!',
								description: <p>You are now following {this.props.location.state.displayName}</p>
							}
						);

                    })
				}
				else{
					console.log(httpResponse)
					toast(
						{
							type: 'error',
							icon: 'warning',
							title: 'Error: User could not be followed!'
						}
					);
				}
            })
            .catch((error) => {
                console.error(error);
        });
	}

    componentDidMount(){
        this.fetchProfile();
    }

	getAboutPane() {
        return (
            <AboutProfileComponent
                fullAuthorId={this.props.location.state.fullAuthorId}
                profile_id={this.state.id}
                host={this.state.host}
                displayName={this.state.displayName}
                url={this.state.url}
                github={this.state.github}
                firstName={this.state.firstName}
                lastName={this.state.lastName}
                email={this.state.email}
                bio={this.state.bio}
                onSuccess={this.fetchProfile}
            />
        );
    }

    getPostsPane() {
		const storeItems = store.getState().loginReducers;
		const urlPath = "/api/author/" + utils.getShortAuthorId(this.props.location.state.fullAuthorId) + "/posts/"
	    return (
	    <span className="streamFeedInProfile">
	        <Tab.Pane>
	        	<StreamFeed storeItems={storeItems} urlPath={urlPath} />
	        </Tab.Pane>
       </span>
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
              ];

	render() {
        return(	
            <div className="pusher AuthorPage">
                <div className="profile">
                    <ProfileBubble
                        displayName={this.state.displayName}
                        userID={this.props.location.state.fullAuthorId}
                        profileBubbleClassAttributes={"ui centered top aligned circular bordered small image"}
                    />
                    <br/>
                    <div className="profile-username">
                        {this.state.displayName}
                    </div>
                    {this.getFollowButton()}
                </div>
                <div className="profile-tabs">
                    <Tab panes={this.tabPanes}></Tab>
                </div>
                <SemanticToastContainer position="bottom-left"/>
            </div>
        )
    }
}

export default Author;