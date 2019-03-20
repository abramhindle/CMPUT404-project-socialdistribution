import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import {Tab} from "semantic-ui-react";
import ProfileBubble from "../components/ProfileBubble";
import StreamFeed from '../components/StreamFeed';
import AboutProfileComponent from "../components/AboutProfileComponent";
import './styles/Author.css';
import store from '../store/index.js';
import utils from "../util/utils";
import FriendsListComponent from '../components/FriendsListComponent';

class Author extends Component {

    constructor(props) {
		super(props);
		this.state = {
            isEdit: false,
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
		};
		this.fetchProfile = this.fetchProfile.bind(this);
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
                            hostUrl: hostUrl,
                            friends: results.friends,
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }

    componentDidMount(){
        this.fetchProfile();
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
                    <button id="addAuthorButton" className="positive ui button">
                        <i className="user plus icon"></i>
                        Request Friend
                    </button>
                </div>
                <div className="profile-tabs">
                    <Tab panes={this.tabPanes} ></Tab>
                </div>
            </div>
        )
    }
}

export default Author;