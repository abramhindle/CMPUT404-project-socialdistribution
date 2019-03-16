import React, { Component } from 'react';
import "./styles/FriendsListComponent.css";
import Truncate from 'react-truncate';
import { Card, Button, Image } from "semantic-ui-react";

class FriendListComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {

		}
		this.renderAllCards = this.renderAllCards.bind(this);
		this.renderFriendCard = this.renderFriendCard.bind(this);
	}	

	testimgs = ["http://img2.wikia.nocookie.net/__cb20120821024317/spongebob/images/e/e8/Spongebob_%28Just_One_Bite%29.jpg",
		"https://format-com-cld-res.cloudinary.com/image/private/s--prMgy-sA--/c_limit,g_center,h_700,w_65535/a_auto,fl_keep_iptc.progressive,q_95/v1/b833558b2310c5ef024506d448441579/Daesha_headshots_vancouver_photographer_fuoco_photography_studio_event_food_portrait_beauty.jpg",
		"https://1bcga31bsykc1tznp22dz571-wpengine.netdna-ssl.com/wp-content/uploads/gabby.jpg",
		"https://dpheadshotswest.com/wp-content/uploads/2018/04/LA-headshots-los-angeles-headshots-actor-headshots-dylan-patrick-124.jpg",
		"http://londonheadshots.net/wp-content/uploads/2015/01/HEADSHOTS_ROSIE_SAT20THMAY20170354.jpg"
		]



	deleteUserUpdate(authorObj){
		this.props.rejectRequest(authorObj)
	}	

	rejectFriendRequest(authorObj){
		this.props.acceptRequest(authorObj)
	}

	renderButtons(authorObj){
		if(this.props.mode === "friends"){
			return(
				<div>
					<Button color='red' onClick={() => {this.deleteUserUpdate(authorObj)}}>Delete</Button>
				</div>
			)
		}
		else if(this.props.mode === "requests"){
			return(
				<div>
					<Button color='green' onClick={() => {this.rejectFriendRequest(authorObj)}}>Accept</Button>
				</div>
			)
		}
	}

	renderFriendCard(d, idx) {
		return(
		<div className="three wide column" key={"grid"+idx}>
			<Card>
				<Image src={this.testimgs[Math.floor(Math.random() * 5)]} />
				<Card.Content>
					<Card.Header>
						<i className="user icon"></i>
						<a href={"http://localhost:3000"+d.url.substring(d.url.indexOf("/author/"),)}>
						{d.displayName}
						</a>
					</Card.Header>
					<Card.Meta>
						<span className="name">{d.firstName+" "+d.lastName}</span>
					</Card.Meta>
					<Card.Description>
						<Truncate lines={3} ellipsis={<span>... <a href={d.url}>Read more</a></span>}>
							{d.bio}
						</Truncate>
					</Card.Description>
				</Card.Content>
				<Card.Content extra>
					<i className="server icon"></i>
					<Truncate lines={1} ellipsis={<span>... <a href={d.url}>Visit profile</a></span>}>
						{d.host}
					</Truncate>
					<br/>
					<a href={d.github}>
						<i className="github icon"></i>
						{d.github}
					</a>
					<br/>
					<a href={"mailto:"+d.email}>
						<i className="envelope icon"></i>
						{d.email}
					</a>
					<br/>
					{this.renderButtons(d)}
				</Card.Content>
			</Card>
		</div>
		)
	}

	renderAllCards(){
		
		// SELECT RANDOM IMAGE TEMP CODE
		let testimgs = ["http://img2.wikia.nocookie.net/__cb20120821024317/spongebob/images/e/e8/Spongebob_%28Just_One_Bite%29.jpg",
		"https://format-com-cld-res.cloudinary.com/image/private/s--prMgy-sA--/c_limit,g_center,h_700,w_65535/a_auto,fl_keep_iptc.progressive,q_95/v1/b833558b2310c5ef024506d448441579/Daesha_headshots_vancouver_photographer_fuoco_photography_studio_event_food_portrait_beauty.jpg",
		"https://1bcga31bsykc1tznp22dz571-wpengine.netdna-ssl.com/wp-content/uploads/gabby.jpg",
		"https://dpheadshotswest.com/wp-content/uploads/2018/04/LA-headshots-los-angeles-headshots-actor-headshots-dylan-patrick-124.jpg",
		"http://londonheadshots.net/wp-content/uploads/2015/01/HEADSHOTS_ROSIE_SAT20THMAY20170354.jpg"
		]
		
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


export default (FriendListComponent);