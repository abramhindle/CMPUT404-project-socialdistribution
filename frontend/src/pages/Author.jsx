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
            errorMessage: "",
            profileReady: false
		};
        this.fetchProfile = this.fetchProfile.bind(this);
        this.sendFollowRequest = this.sendFollowRequest.bind(this);
        this.getFollowButton = this.getFollowButton.bind(this);
        this.sendUnfollowRequest = this.sendUnfollowRequest.bind(this);
        this.getFollowStatus = this.getFollowStatus.bind(this);
        // this.getTabPanes = this.getTabPanes.bind(this);
        this.checkCanFollow = this.checkCanFollow.bind(this);
	}

	checkCanFollow() {
        console.log("isForeignFriend")
        let authenticatedAuthorId = store.getState().loginReducers.userId || Cookies.get("userID");
        const hostUrl = "/api/author/"+ utils.prepAuthorIdForRequest(authenticatedAuthorId, encodeURIComponent(authenticatedAuthorId));
        HTTPFetchUtil.getRequest(hostUrl, true)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        console.log(results);
                        if (results.friends) {
                            for (let i = 0; i < results.friends.length; i++) {
                                if (results.friends[i].id === authenticatedAuthorId){
                                    this.setState({canFollow: false});
                                    return;
                                }
                            }
                        }
                    })
                } else {
                    httpResponse.json().then((results) => {
                       this.setState({
                           error: true,
                           errorMessage: results,
                           canFollow: true
                        });
                    });
                }
            })
            .catch((error) => {
                console.error(error);
        });
        this.setState({canFollow: true});
    }

	fetchProfile() {
        let authenticatedAuthorId = store.getState().loginReducers.userId || Cookies.get("userID");
        const hostUrl = "/api/author/"+ utils.prepAuthorIdForRequest(authenticatedAuthorId, this.props.match.params.authorId),
            requireAuth = true;
        this.setState({
            profileReady: false
        });
        HTTPFetchUtil.getRequest(hostUrl, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        let canFollow = true;
                        if (results.friends) {
                            for (let i = 0; i < results.friends.length; i++) {
                                if (results.friends[i].id === authenticatedAuthorId){
                                    canFollow = false;
                                    break;
                                }
                            }
                        } else {
                            // results.friends not available means it is a foreign friend
                            // then we need to fetch our own profile to check if i am friend/following him already
                            this.checkCanFollow();
                        }

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
                            isSelf: results.id === authenticatedAuthorId,
                            canFollow: canFollow,
                            error: false,
                            profileReady: true
                        });
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
        let followButton = null;
        if (this.state.profileReady) {
            console.log("get follow button");
            console.log(this.state.isFollowing , this.state.canFollow)
            if (this.state.isSelf) {
                return null;
            }

            if (this.state.canFollow) {
                followButton = <Button positive onClick={this.sendFollowRequest}><Icon name = "user plus" />Follow</Button>
            } else {
                followButton = <Button negative onClick={this.sendUnfollowRequest}><Icon name = "user times"/>Unfollow</Button>
            }
        }
        return <div>{followButton}</div>;

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
        const authorID = this.getloggedinAuthorIDandHost(),
            urlPath = "/api/followers/" + this.props.match.params.authorId,
            requireAuth = true;
        HTTPFetchUtil.getRequest(urlPath, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        let canFollow = true;
                        for (let i = 0; i < results.authors.length; i++) {
                            if (results.authors[i].id === authorID[0]){
                                canFollow = false;
                                break;
                            }
                        }
                        this.setState({
                            canFollow: canFollow,
                            error: false
                        });
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
            this.getFollowStatus();
        }
    }

	getAboutPane() {
        return (
            <AboutProfileComponent
                fullAuthorId={decodeURIComponent(this.props.match.url)}
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
        // todo: make this cross server compatible
		const storeItems = store.getState().loginReducers;
		const urlPath = "/api/author/" + utils.getShortAuthorId(decodeURIComponent(this.props.match.url)) + "/posts/";
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

    // getFullAuthorIdFromURL(path) {
    //     const tmp = path.split("/author/");
    //     return utils.unEscapeAuthorId(tmp[1])
    // }

    tabPanes = [
                { menuItem: 'About', render: () => this.getAboutPane()},
                { menuItem: 'Posts', render: () => this.getPostsPane()},
                { menuItem: 'Friends', render: () =>  this.getFriendsPane()}
              ];

    // getTabPanes() {
    //     console.log("getTabPanes", this.state.friends);
    //
    //     if(this.state.friends) {
    //         return [
    //             { menuItem: 'About', render: () => this.getAboutPane()},
    //             { menuItem: 'Posts', render: () => this.getPostsPane()},
    //             { menuItem: 'Friends', render: () =>  this.getFriendsPane()}
    //         ];
    //     } else {
    //         return [
    //             { menuItem: 'About', render: () => this.getAboutPane()},
    //             { menuItem: 'Posts', render: () => this.getPostsPane()}
    //         ];
    //     }
    // }

	render() {
        return(	
            <div className="pusher AuthorPage">
            	<h1 className="authorHeader"> {this.state.displayName} </h1>
                <div className="profile">
                    <ProfileBubble
                        displayName={this.state.displayName}
                        userID={decodeURIComponent(this.props.match.url)}
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
