import React, { useState } from "react";
import { Avatar, ButtonGroup, Panel, Button } from "rsuite";

function PROFILE() {
	const [posts, setPosts] = React.useState(true);
	const [appearance, setAppearance] = React.useState({
		posts: "primary",
		friends: "ghost",
	});

	const handlePostsBtnClick = () => {
		setPosts(true);
		setAppearance({ posts: "primary", friends: "ghost" });
	};

	const handleFriendsBtnClick = () => {
		setPosts(false);
		setAppearance({ posts: "ghost", friends: "primary" });
	};

	// make a get request to get author and every post the author made and comments on the posts 

	return (
		<Panel shaded style={{ width: "50%", margin: "auto" }}>
			<Avatar
				style={{ float: "left" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
				size="lg"
			></Avatar>
			<h2 style={{ marginLeft: "10px", float: "left" }}>Author</h2>

			<ButtonGroup justified style={{ paddingTop: "10px" }}>
				<Button
					style={{ textAlign: "center" }}
					appearance={appearance["posts"]}
					onClick={handlePostsBtnClick}
				>
					Posts
				</Button>
				<Button
					style={{ textAlign: "center" }}
					appearance={appearance["friends"]}
					onClick={handleFriendsBtnClick}
				>
					Friends
				</Button>
			</ButtonGroup>
			{posts ? <div>posts</div> : <div>friends</div>}
		</Panel>
	);
}

export default PROFILE;
