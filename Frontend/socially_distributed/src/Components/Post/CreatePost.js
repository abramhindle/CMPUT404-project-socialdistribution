import React, { useState } from "react";
import { Input, Avatar, Panel, Dropdown, Uploader, Button } from "rsuite";
// import { Scrollbars } from "react-custom-scrollbars-2";
// Component Imports
import axios from "axios";

function CREATEPOST() {
	const [post_status, set_post_status] = useState("Public");
	const [post_type, set_post_type] = useState("Text");
	const [text, setText] = useState("");
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");

	const input = () => {
		if (post_type === "Text") {
			return (
				<div>
					<Input
						style={{ float: "left", marginTop: "5px" }}
						as="textarea"
						rows={5}
						placeholder="Text"
						onChange={(e) => setText(e)}
					/>
				</div>
			);
		}

		if (post_type === "Image") {
			return (
				<div>
					<Uploader
						action="post/authors/{AUTHOR_ID}/posts/"
						autoUpload={false}
						draggable
						style={{
							float: "left",
							width: "100%",
							margin: "auto",
							paddingTop: "5px",
						}}
					>
						<div
							style={{
								height: "100px",
								display: "flex",
								alignItems: "center",
								justifyContent: "center",
							}}
						>
							<span>
								Click or Drag files to this area to upload
							</span>
						</div>
					</Uploader>
				</div>
			);
		}
	};

	const handlePostClick = () => {
		const author = JSON.parse(localStorage.getItem("user"));
		const len = "2a647e52-3345-4dd7-b2ab-91eec3bc9340".length;
		const author_id = author.id.slice(
			author.id.length - len,
			author.id.length
		);
		const url = "posts/authors/" + author_id + "/posts/";
		var params = {
			title: title,
			description: description,
			content: text,
			contentType: "text/plain",
			author: author,
		};
		console.log(JSON.stringify(params));
		axios({ method: "post", url: url, data: params })
			.then((res) => {
				console.log(res);
			})
			.catch((err) => console.log(err));
	};

	return (
		<div
			style={{
				marginBottom: "5px",
				height: "auto",
				border: "1px solid black",
				borderRadius: "10px",
				padding: "5px",
				position: "relative",
			}}
		>
			<Avatar
				style={{ float: "left" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			/>
			<Dropdown
				title={post_status}
				activeKey={post_status}
				onSelect={(eventkey) => set_post_status(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="Public">Public</Dropdown.Item>
				<Dropdown.Item eventKey="Friends">Friends</Dropdown.Item>
				<Dropdown.Item eventKey="Private">Private</Dropdown.Item>
			</Dropdown>
			<Dropdown
				title={post_type}
				activeKey={post_type}
				onSelect={(eventkey) => set_post_type(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="Text">text</Dropdown.Item>
				<Dropdown.Item eventKey="Image">image</Dropdown.Item>
			</Dropdown>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="Title"
				onChange={(e) => setTitle(e)}
			/>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="description"
				onChange={(e) => setDescription(e)}
			/>
			{input()}
			<Button
				style={{ marginTop: "3px" }}
				onClick={handlePostClick}
				appearance="primary"
				block
			>
				Post
			</Button>
		</div>
	);
}

export default CREATEPOST;
