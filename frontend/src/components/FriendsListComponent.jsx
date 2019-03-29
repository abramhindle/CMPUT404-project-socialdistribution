import React, { Component } from 'react';
import "./styles/FriendsListComponent.css";
import Truncate from 'react-truncate';
import { Card, Button } from "semantic-ui-react";
import PropTypes from 'prop-types';
import {Link} from "react-router-dom";
import ProfileBubble from "../components/ProfileBubble";

class FriendListComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {

		}
		this.renderAllCards = this.renderAllCards.bind(this);
		this.renderFriendCard = this.renderFriendCard.bind(this);
	}	

	renderServerDetails(authorObj){
		if(authorObj.url !== ""){
			return(
			<div>
				<i className="server icon"></i>
				<Link to={"/author/" + encodeURIComponent(authorObj.id)}>
				<Truncate lines={1} width={220}>
				{authorObj.url}
				</Truncate>
				</Link>
			</div>
			)
		}
	}

	renderGithubDetails(authorObj){
		if(authorObj.github !== ""){
			return(
				<div>
					<a href={authorObj.github} target={"_blank"}>
					<i className="github icon"></i>
					<Truncate lines={1} width={220}>
					{authorObj.github}
					</Truncate>
					</a>
				</div>
			)
		}
	}

	renderEmailDetails(authorObj){
		if(authorObj.email !== ""){
			return(
				<div>
					<a href={"mailto:"+authorObj.github} target={"_blank"}>
					<i className="envelope icon"></i>
					<Truncate lines={1} width={220}>
					{authorObj.email}
					</Truncate>
					</a>
				</div>
			)
		}
	}

	renderDisplayName(authorObj){
		if(authorObj.displayName !== "" ){
			return(
					<div>
						<i className="user icon"></i>
							<Link to={"/author/" + encodeURIComponent(authorObj.id)}>
								{authorObj.displayName}
							</Link>
						<Truncate lines={1} width={220}>
						</Truncate>
					</div>
			)
		}
	}
	renderButtons(authorObj){
		if(this.props.mode === "friends" && this.props.viewOwnFriendlist){
			return(
				<div>
					<Button color='red' onClick={() => {this.props.rejectRequest(authorObj)}}>Delete</Button>
				</div>
			)
		}
		else if(this.props.mode === "requests" && this.props.viewOwnFriendlist){
			return(
				<div>
					<Button color='green' onClick={() => {this.props.acceptRequest(authorObj)}}>Accept</Button>
				</div>
			)
		}
	}

	renderFriendCard(authorObj, authorIndex) {
		return(
		<div className="three wide column" key={"grid"+authorIndex}>
			<Card>
				<span className="profileBubbleFriend">
            	<ProfileBubble
                    displayName={authorObj.displayName}
                	userID={decodeURIComponent(authorObj.authorId)}
                    profileBubbleClassAttributes={"ui centered top aligned circular bordered small image"}
                />
                </span>
				<Card.Content className="friendCardContent">
					<Card.Header className="displayNameWithIcon">
					{this.renderDisplayName(authorObj)}
					</Card.Header>
					<Card.Meta>
						<span className="name">{authorObj.firstName+" "+authorObj.lastName}</span>
					</Card.Meta>
					<Card.Description>
						<Truncate lines={3} ellipsis={<span>...</span>}>
							{authorObj.bio}
						</Truncate>
					</Card.Description>
				</Card.Content>
				<Card.Content extra>
					{this.renderServerDetails(authorObj)}
					{this.renderGithubDetails(authorObj)}
					{this.renderEmailDetails(authorObj)}
					{this.renderButtons(authorObj)}
				</Card.Content>
			</Card>
		</div>
		)
	}

	renderAllCards(){
		const blackText = this.props.blackText ? {color: "black"} : {};
		if (!this.props.data) {
			return (
				<h1 id="noList" style={blackText}>Foreign Friend List Unavailable</h1>
			)
		}
		if(this.props.data.length > 0){
			return (
				this.props.data.map(this.renderFriendCard));
			}
		else{
			return (<h1 id="noList" style={blackText}>None</h1>)
		}
		
	}
    render() {
		return(
			<div className="ui grid">	
				{this.renderAllCards()}
			</div>
		)
	}
}

FriendListComponent.propTypes = {
	acceptRequest: PropTypes.func,
	data: PropTypes.array,
	mode: PropTypes.string.isRequired,
	rejectRequest: PropTypes.func,
	viewOwnFriendlist: PropTypes.bool.isRequired,
	blackText: PropTypes.bool
};

export default (FriendListComponent);