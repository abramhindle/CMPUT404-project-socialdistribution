import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import {Tab, Button, Icon, Message} from "semantic-ui-react";
import ProfileBubble from "../components/ProfileBubble";
import StreamFeed from '../components/StreamFeed';
import AboutProfileComponent from "../components/AboutProfileComponent";
import './styles/Author.css';
import utils from "../util/utils";
import { SemanticToastContainer, toast } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';
import store from "../store/index";
import Cookies from 'js-cookie';
import FriendsListComponent from '../components/FriendsListComponent';


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
            friends: [],
            error: false,
            errorMessage: ""
		};
        this.fetchProfile = this.fetchProfile.bind(this);
        this.sendFollowRequest = this.sendFollowRequest.bind(this);
        this.getFollowButton = this.getFollowButton.bind(this);
        this.sendUnfollowRequest = this.sendUnfollowRequest.bind(this);
        this.getFollowStatus = this.getFollowStatus.bind(this);
	}

	fetchProfile() {
        //todo deal with other hosts
        const hostUrl = "/api/author/"+ utils.getShortAuthorId(this.props.location.state.fullAuthorId),
            requireAuth = true;
        HTTPFetchUtil.getRequest(hostUrl, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        const authorID = this.getloggedinAuthorIDandHost();
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
                            hostUrl: hostUrl,
                            friends: results.friends,
                            isSelf: results.id === authorID[0],
                            error: false
                        })
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
        });
    }

    getFollowButton() {
        let followbutton;
        if (this.state.isSelf) {
            return null;
        }

        else if (!this.state.isFollowing && !this.state.isSelf) {
            followbutton = <Button positive onClick={this.sendFollowRequest}><Icon name = "user plus" />Follow</Button>
        }

        else if (this.state.isFollowing && !this.state.isSelf) {
            followbutton = <Button negative onClick={this.sendUnfollowRequest}><Icon name = "user times"/>Unfollow</Button>
        }

        return <div>{followbutton}</div>;

    }

    getloggedinAuthorIDandHost() {
        const cookieauthorid = Cookies.get("userID"),
            storeauthorid = store.getState().loginReducers.userId,
            cookiehost = cookieauthorid.split("author/")[0],
            storehost = store.getState().loginReducers.hostName;
        let authorID;
        let host;
        if (cookieauthorid !== null) {
            authorID = cookieauthorid;
        } else if (storeauthorid !== null) {
            authorID = storeauthorid;
        }
        if (cookiehost !== null) {
            host = cookiehost;
        } else if (storehost !== null) {
            host = storehost;
        }
        return [authorID, host]
    }

    getFollowStatus() {
        const authorID = this.getloggedinAuthorIDandHost();
        let urlPath = "/api/followers/" + utils.getShortAuthorId(this.props.location.state.fullAuthorId),
            requireAuth = true;
        HTTPFetchUtil.getRequest(urlPath, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        for (let i = 0; i < results.authors.length; i++) {
                            if (results.authors[i].id === authorID[0]){
                                this.setState({
                                    isFollowing: true,
                                    error: false
                                })
                            }
                        }
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
        });
        }

    sendUnfollowRequest() {
        const authorID = this.getloggedinAuthorIDandHost();
        let urlPath = "/api/unfollow/";
		let body = {
			query: "unfollow",
			author: {
				id: authorID[0],
				host: authorID[1],
			},
			friend:{
				id: this.state.id,
				host: this.state.host,
			}
		};
		HTTPFetchUtil.sendPostRequest(urlPath, true, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.setState({
                            isFollowing: false
                        });
						toast(
							{
								type: 'success',
								icon: 'user',
								title: 'Unfollow successful!',
								description: <p>You are no longer following {this.state.displayName}</p>
							}
						);

                    })
				}
				else{
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
        var authorID;
        authorID = this.getloggedinAuthorIDandHost();
		let urlPath = "/api/friendrequest/";
		let body = {
			query: "friendrequest",
			author: {
				id: authorID[0],
				host: authorID[1],
			},
			friend:{
				id: this.state.id,
				host: this.state.host,
			}
		};
		HTTPFetchUtil.sendPostRequest(urlPath, true, body)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.setState({
                            isFollowing: true
                        });
						toast(
							{
								type: 'success',
								icon: 'user',
								title: 'Follow successful!',
								description: <p>You are now following {this.state.displayName}</p>
							}
						);

                    })
				}
				else{
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
        this.getFollowStatus();
    }

    componentDidUpdate(prevProps){
        if(prevProps.match.url !== this.props.match.url){
            this.fetchProfile();
        }
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
		const urlPath = "/api/author/" + utils.getShortAuthorId(this.props.location.state.fullAuthorId) + "/posts/";
	    return (
	    <span className="streamFeedInProfile">
	        <Tab.Pane>
	        	<StreamFeed storeItems={storeItems} urlPath={urlPath} displayCreatePostButton={false} />
	        </Tab.Pane>
       </span>
        );
    }


    getFriendsPane() {
	    return (
	        <Tab.Pane><FriendsListComponent data={this.state.friends} viewOwnFriendlist={false} mode="friends"/></Tab.Pane>
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
            	<h1 className="authorHeader"> {this.state.displayName} </h1>
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
                    <Message negative hidden={!this.state.error}>
                        <Message.Header>Fetch Profile Failed</Message.Header>
                        <p>{this.state.errorMessage}</p>
                    </Message>
                    <Tab panes={this.tabPanes}></Tab>
                </div>
                <SemanticToastContainer position="bottom-left"/>
            </div>
        )
    }
}

export default Author;
