import React, { useState } from "react";
import { Input, Avatar, InputGroup, Panel, IconButton } from "rsuite";
import { Scrollbars } from "react-custom-scrollbars-2";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import ShareIcon from "@rsuite/icons/legacy/Reply";
import COMMENTS from "./Comment";
// Component Imports

function POST({ postobj }) {
	const [post, set_post] = useState(postobj);
	const [comment, set_comment] = useState("");

	const body = () => {
		if (post["contentType"] === "text/plain") {
			return <p style={{ padding: "5px" }}>{post["content"]}</p>;
		}

		// Peter you just need to return the image here
		if (post["contentType"] === "image/jpeg") {
			return <p>{}</p>;
		}
	};

	// need to make a get request to get the post obj and set post obj to that.

	return (
		<div
			style={{
				display: "grid",
				gridTemplateColumns: "2fr 1fr",
				height: "50vh",
				marginBottom: "5px",
				border: "1px solid black",
				borderRadius: "10px",
			}}
		>
			<div style={{ padding: "5px" }}>
				<div
					style={{
						height: "50px",
						borderBottom: "0.5px solid grey",
					}}
				>
					<Avatar
						style={{ float: "left" }}
						circle
						src="https://avatars.githubusercontent.com/u/12592949"
					></Avatar>
					<h5
						style={{
							marginLeft: "10px",
							float: "left",
						}}
					>
						{post["author"]["displayName"]}
					</h5>
					<IconButton
						style={{ float: "right", marginRight: "10px" }}
						appearance="subtle"
						icon={<ShareIcon />}
					/>
					<IconButton
						style={{ float: "right", marginRight: "10px" }}
						appearance="subtle"
						icon={<ThumbsUpIcon />}
					/>
				</div>
				<Scrollbars style={{ height: "330px" }}>
					<div>
						<h3>{post["title"]}</h3>
						<h5>{post["description"]}</h5>
						{body()}
					</div>
				</Scrollbars>
			</div>
			<COMMENTS postobj={postobj}></COMMENTS>
		</div>
	);
}

export default POST;
