import React, { useState } from "react";
import { Avatar, Panel, IconButton } from "rsuite";
import ThumbsUpIcon from "@rsuite/icons/legacy/ThumbsUp";
import ShareIcon from "@rsuite/icons/legacy/Reply";
import COMMENTS from "./Comment";
import "./Post.css";
import ReactMarkdown from "react-markdown";
import LIKE from "./Like";
import EditIcon from "@rsuite/icons/Edit";
import TrashIcon from "@rsuite/icons/Trash";
import EDITPOSTMODAL from "../Modals/EditPostModal";
// Component Imports

function POST({ postobj, edit }) {
	const [post, set_post] = useState(postobj);
	const [comment, set_comment] = useState("");
	const [authorPosts, set_authorPosts] = useState(edit);
	const [open, setOpen] = useState(false);

	const body = () => {
		if (post["contentType"] === "text/plain") {
			return <p style={{ padding: "5px" }}>{post["content"]}</p>;
		}

		if (post["contentType"] === "text/markdown") {
			return (
				<ReactMarkdown style={{ padding: "5px", height: "100px" }}>
					{post["content"]}
				</ReactMarkdown>
			);
		}

		// Peter you just need to return the image here
		if (post["contentType"] === "image/jpeg") {
			return <p>{}</p>;
		}
	};

	const delEditBtn = (
		<div>
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				onClick={handleOpen}
				icon={<EditIcon />}
			/>
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				icon={<TrashIcon />}
			/>
		</div>
	);

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
			<div
				style={{
					marginLeft: "10px",
					float: "left",
				}}
			>
				{post["author"]["displayName"]}
			</div>
			<IconButton
				style={{ float: "right", marginRight: "10px" }}
				appearance="subtle"
				icon={<ShareIcon />}
			/>
			<LIKE postObj={postobj} />
			{edit ? delEditBtn : <div />}
		</div>
	);

	const handleOpen = () => {
		setOpen(true);
	};

	const handleModalClose = () => {
		setOpen(false);
	};

	return (
		<div>
			<Panel
				bordered
				header={header}
				style={{
					marginBottom: "5px",
				}}
			>
				<div style={{ height: "auto" }}>
					<div
						style={{
							marginLeft: "5px",
							fontFamily: "Times New Roman",
							fontWeight: "bold",
							fontSize: "20px",
						}}
					>
						{post["title"]}
					</div>
					<div
						style={{
							marginLeft: "5px",
							fontFamily: "Times New Roman",
							fontWeight: "bold",
							fontSize: "15px",
						}}
					>
						{post["description"]}
					</div>
					{body()}
				</div>
				<Panel bordered collapsible header="Comments">
					<COMMENTS postobj={postobj}></COMMENTS>
				</Panel>
			</Panel>
			<EDITPOSTMODAL
				open={open}
				obj={postobj}
				handleClose={handleModalClose}
			/>
		</div>
	);
}

export default POST;
