import React, { Component } from 'react';
import "./styles/FriendsListComponent.css";
import Truncate from 'react-truncate';

class FriendListComponent extends Component {	

	constructor(props) {
		super(props);
		this.state = {

		}
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
				this.props.data.map(function(d, idx){
				return(
				<div className="three wide column" key={"grid"+idx}>
					<div className="ui card" key={"card"+idx}>
						<div className="image">
							<img alt="profile" src={testimgs[Math.floor(Math.random() * 5)]}></img>
						</div>
						<div className="content">
							<i className="user icon"></i>
							<a href={d.url}>
							{d.displayName}
							</a>
								<div className="meta">
									<Truncate lines={1} ellipsis={<span>...</span>}>
									<span className="date">{d.firstName+" "+d.lastName}</span>
									</Truncate>
								</div>
								<div className="description">
									<Truncate lines={3} ellipsis={<span>... <a href={d.url}>Read more</a></span>}>
										{d.bio}
									</Truncate>
								</div>
						</div>
						<div className="extra content">
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
						</div>
					</div>
				</div>
				)
			}));
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