import React, { useState } from "react";
import { Avatar, Panel, IconButton } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import ShareIcon from "@rsuite/icons/legacy/Reply";
import COMMENTS from "./Comment";
import "./Post.css";
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

	const header = (
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
			<h4
				style={{
					marginLeft: "10px",
					float: "left",
				}}
			>
				{post["author"]["displayName"]}
			</h4>
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
	);

	return (
		<Panel
			bordered
			header={header}
			style={{
				marginBottom: "5px",
			}}
		>
			<div style={{ height: "auto" }}>
				<h3>{post["title"]}</h3>
				<h5>{post["description"]}</h5>
				{body()}
			</div>
			<Panel bordered collapsible header="Comments">
				<COMMENTS postobj={postobj}></COMMENTS>
			</Panel>
		</Panel>
	);
}

export default POST;
