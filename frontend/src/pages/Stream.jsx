import React, { Component } from 'react';
import StreamFeed from '../components/StreamFeed';
import { SemanticToastContainer } from 'react-semantic-toasts';
import store from '../store/index.js';
import './styles/Stream.css';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import utils from "../util/utils";
import Cookies from 'js-cookie';

class Stream extends Component {
	constructor(props) {
		super(props);
		this.state = {
			github: '',
		};	
		this.fetchProfile = this.fetchProfile.bind(this);
		this.getloggedinAuthorID = this.getloggedinAuthorID.bind(this);
	};	
	
    getloggedinAuthorID() {
        const cookieauthorid = Cookies.get("userID"),
            storeauthorid = store.getState().loginReducers.userId;
        let authorID;
        if (cookieauthorid !== null) {
            authorID = cookieauthorid;
        } else if (storeauthorid !== null) {
			authorID = storeauthorid;
		}
	return authorID;
	}

	fetchProfile() {
		const authorID = this.getloggedinAuthorID();
		const hostUrl = "/api/author/"+ utils.getShortAuthorId(authorID),
				requireAuth = true;
		HTTPFetchUtil.getRequest(hostUrl, requireAuth)
				.then((httpResponse) => {
						if (httpResponse.status === 200) {
								httpResponse.json().then((results) => {
									this.setState({
										github: results.github,
									});
								})
						} else {
							throw new Error('Could not get github username');
						}
				})
				.catch((error) => {
						console.error(error);
		});
	}

	componentDidMount() {
		this.fetchProfile();
	}
		
	render() {
		const storeItems = store.getState().loginReducers;
		return(	
			<div className="pusher">
				<h1 className="streamHeader"> Stream </h1>

				{this.state.github
				?
				<StreamFeed storeItems={storeItems} githuburl={this.state.github} urlPath="/api/author/posts/" />
				:
				<StreamFeed storeItems={storeItems} urlPath="/api/author/posts/" />
				}
				
                <SemanticToastContainer position="bottom-left"/>
			</div>
			)
    }
}

export default Stream;
