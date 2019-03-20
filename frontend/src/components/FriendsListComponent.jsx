import React, { Component } from 'react';
import "./styles/FriendsListComponent.css";
import Truncate from 'react-truncate';
import { Card, Button, Image } from "semantic-ui-react";
import utils from "../util/utils";
import PropTypes from 'prop-types';
import {Link} from "react-router-dom";

class FriendListComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {

		}
		this.renderAllCards = this.renderAllCards.bind(this);
		this.renderFriendCard = this.renderFriendCard.bind(this);
	}	
	//TODO: Future image handling implementation here
	testimgs = ["http://img2.wikia.nocookie.net/__cb20120821024317/spongebob/images/e/e8/Spongebob_%28Just_One_Bite%29.jpg",
		"https://format-com-cld-res.cloudinary.com/image/private/s--prMgy-sA--/c_limit,g_center,h_700,w_65535/a_auto,fl_keep_iptc.progressive,q_95/v1/b833558b2310c5ef024506d448441579/Daesha_headshots_vancouver_photographer_fuoco_photography_studio_event_food_portrait_beauty.jpg",
		"https://1bcga31bsykc1tznp22dz571-wpengine.netdna-ssl.com/wp-content/uploads/gabby.jpg",
		"https://dpheadshotswest.com/wp-content/uploads/2018/04/LA-headshots-los-angeles-headshots-actor-headshots-dylan-patrick-124.jpg",
		"http://londonheadshots.net/wp-content/uploads/2015/01/HEADSHOTS_ROSIE_SAT20THMAY20170354.jpg",
		"https://upload.wikimedia.org/wikipedia/commons/5/5f/Alberto_conversi_profile_pic.jpg",
		];

	renderServerDetails(authorObj){
		if(authorObj.url !== ""){
			return(
			<div>
				<i className="server icon"></i>
				<Link to={
							{pathname: "/author/"+utils.getStripedEscapedAuthorId(authorObj.url.substring(7,)),
							  state: {
							  	fullAuthorId: authorObj.url,
							  }}}>
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
							<Link to={
								{pathname: "/author/"+utils.getStripedEscapedAuthorId(authorObj.url.substring(7,)),
									state: {
										fullAuthorId: authorObj.url,
									}}}>{authorObj.displayName}</Link>
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
				<Image src={this.testimgs[Math.floor(Math.random() * 6)]} />
				<Card.Content>
					<Card.Header>
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
		if(this.props.data.length > 0){
			return (
				this.props.data.map(this.renderFriendCard));
			}
		else{
			return (<h1 id="noList">None</h1>)
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
	data: PropTypes.array.isRequired,
	mode: PropTypes.string.isRequired,
	rejectRequest: PropTypes.func,
	viewOwnFriendlist: PropTypes.bool.isRequired,
};

export default (FriendListComponent);