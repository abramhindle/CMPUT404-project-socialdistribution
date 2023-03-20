import React, { useState, useEffect } from "react";
import {
	Input,
	Avatar,
	useToaster,
	Message,
	Dropdown,
	Uploader,
	Button,
} from "rsuite";
import axios from "axios";
import "react-toastify/dist/ReactToastify.css";
import { getAuthorId } from "../utils/auth";
import PROFILEIMAGE from "../Profile/ProfileImage";

function EDITPOST({ obj, handleClose }) {
	const [post_status, set_post_status] = useState("Public");
	const [post_type, set_post_type] = useState("text/plain");
	const [text, setText] = useState("");
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");
	const [categories, setCategories] = useState("");
	const [markdown, setMarkdown] = useState("");
	const toaster = useToaster();

	const stringify = (arr) => {
		let str = "";
		for (let i = 0; i < arr.length; i++) {
			str = str + arr[i];
		}
		return str;
	};

	useEffect(() => {
		let x = stringify(obj.categories);
		setText(obj.content);
		setDescription(obj.description);
		setTitle(obj.title);
		setCategories(x);
		set_post_status(obj.visibility);
		set_post_type(obj.contentType);
		setMarkdown(obj.content);
	}, []);

	const input = () => {
		if (post_type === "text/plain") {
			return (
				<div>
					<Input
						style={{
							float: "left",
							marginTop: "5px",
							marginBottom: "5px",
						}}
						as="textarea"
						rows={5}
						placeholder="Text"
						value={text}
						onChange={(e) => setText(e)}
					/>
				</div>
			);
		}

		if (post_type === "text/markdown") {
			return (
				<div>
					<Input
						style={{
							float: "left",
							marginTop: "5px",
							marginBottom: "5px",
						}}
						as="textarea"
						rows={5}
						placeholder="Text"
						value={text}
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

	const notifySuccessPost = () => {
		toaster.push(
			<Message type="success">Successful Edited this post</Message>,
			{
				placement: "topEnd",
				duration: 5000,
			}
		);
	};

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const handlePostClick = () => {
		const author_id = getAuthorId(null);
		const post_id = getAuthorId(obj.id);
		const url = `posts/authors/${author_id}/posts/${post_id}/`;
		var params = {
			title: title,
			description: description,
			content: text,
			contentType: post_type,
			visiblity: post_status,
			categories: categories,
		};
		axios({ method: "post", url: url, data: params })
			.then((res) => {
				if (res.status === 200) {
					handleClose();
					notifySuccessPost();
				} else {
					notifyFailedPost(res.data);
				}
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
			<PROFILEIMAGE size="md" />
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
				disabled
				onSelect={(eventkey) => set_post_type(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="text/plain">Plain</Dropdown.Item>
				<Dropdown.Item eventKey="text/markdown">Markdown</Dropdown.Item>
				<Dropdown.Item eventKey="image/png">Png</Dropdown.Item>
				<Dropdown.Item eventKey="image/jpeg">Jpeg</Dropdown.Item>
			</Dropdown>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="Categories"
				value={categories}
				onChange={(e) => setCategories(e)}
			/>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="Title"
				value={title}
				onChange={(e) => setTitle(e)}
			/>
			<Input
				style={{ float: "left", marginTop: "5px" }}
				as="textarea"
				rows={1}
				placeholder="description"
				value={description}
				onChange={(e) => setDescription(e)}
			/>
			{input()}
			<Button
				style={{ marginTop: "3px" }}
				onClick={handlePostClick}
				appearance="primary"
				block
			>
				Post Edit
			</Button>
		</div>
	);
}

export default EDITPOST;
