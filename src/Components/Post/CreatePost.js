import React, { useLayoutEffect, useCallback, useState } from "react";
import {
	Input,
	Avatar,
	useToaster,
	Message,
	Dropdown,
	Uploader,
	Button,
	CheckPicker,
} from "rsuite";
import { reqInstance } from "../utils/axios";
import "react-toastify/dist/ReactToastify.css";
import { getAuthorId } from "../utils/auth";
import { useNavigate } from "react-router-dom";
import PROFILEIMAGE from "../Profile/ProfileImage";

function CREATEPOST() {
	const [post_status, set_post_status] = useState("PUBLIC");
	const [post_type, set_post_type] = useState("text/plain");
	const [text, setText] = useState("");
	const [title, setTitle] = useState("");
	const [description, setDescription] = useState("");
	const [categories, setCategories] = useState("");
	const [disabled, setDisabled] = useState(true);
	const [markdown, setMarkdown] = useState("");
	const [authors, setAuthors] = useState({ items: [] });
	let navigate = useNavigate();
	const toaster = useToaster();
	const data = friends.items.map((item) => ({
		label: item["displayName"],
		value: item["displayName"],
	}));
	const [image64, set_image64] = useState("");
	const [data, setData] = useState([]);

	function handleClick(eventkey) {
		set_post_status(eventkey);
		if (eventkey === "PRIVATE") {
			setDisabled(false);
		} else {
			setDisabled(true);
		}
	}

	useLayoutEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/login");
		} else {
			const AUTHOR_ID = getAuthorId(null);
			const url = `authors/${AUTHOR_ID}/followers/`;
			reqInstance({
				method: "get",
				url: url,
			}).then((res) => {
				setData(
					res.data.items.map((item) => ({
						label: item["displayName"],
						value: item["displayName"],
					}))
				);
			});
		}
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

		// converts image to base64 then passes it into the backend
		/* this is the code for what the uploader was:
		<Uploader
						action="post/authors/{AUTHOR_ID}/posts/"
						accept=".png, .jpg, .jpeg"
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
		*/
		if (post_type === "image/png" || post_type === "image/jpeg") {
			return (
				<div>
					<input id="file" type="file" accept=".png, .jpg, .jpeg" />
				</div>
			);
		}
	};

	const notifySuccessPost = () => {
		toaster.push(<Message type="success">Successful post</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	async function readFileAsDataURL(file) {
		return new Promise((resolve) => {
			let fileReader = new FileReader();
			fileReader.onloadend = (e) => resolve(set_image64(fileReader.result));
			fileReader.readAsDataURL(file);
		});

	}

	async function handlePostClick () {
		const author = JSON.parse(localStorage.getItem("user"));
		const author_id = getAuthorId(null);
		const url = `posts/authors/${author_id}/posts/`;

		var params = {
			title: title,
			description: description,
			content: text,
			contentType: post_type,
			visibility: post_status,
		};

		if (post_status === 'PRIVATE') {
			params['authors'] = authors;

		}
		var imagefile = "";
		if (post_type === "image/png" || post_type === "image/jpeg") {
			imagefile = document.getElementById("file").files[0];
			if (imagefile) {
				await readFileAsDataURL(imagefile).then(async (dataURL) => {
					set_image64(dataURL);
				});
			}
			params["image"] = image64;
		}

		if (categories.length > 0) {
			params["categories"] = categories;
		}

		reqInstance({ method: "post", url: url, data: params })
			.then((res) => {
				if (res.status === 200) {
					notifySuccessPost();
					setText("");
					setDescription("");
					setTitle("");
					setCategories("");
					set_post_status("PUBLIC");
					set_post_type("text/plain");
					setMarkdown("");
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
				onSelect={(eventkey) => handleClick(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="PUBLIC">Public</Dropdown.Item>
				<Dropdown.Item eventKey="FRIENDS">Friends</Dropdown.Item>
				<Dropdown.Item eventKey="PRIVATE">Private</Dropdown.Item>
				<Dropdown.Item eventKey="UNLISTED">Unlisted</Dropdown.Item>
			</Dropdown>
			<Dropdown
				title={post_type}
				activeKey={post_type}
				onSelect={(eventkey) => set_post_type(eventkey)}
				style={{ float: "left", marginLeft: "10px" }}
			>
				<Dropdown.Item eventKey="text/plain">Plain</Dropdown.Item>
				<Dropdown.Item eventKey="text/markdown">Markdown</Dropdown.Item>
				<Dropdown.Item eventKey="image/png">Png</Dropdown.Item>
				<Dropdown.Item eventKey="image/jpeg">Jpeg</Dropdown.Item>
			</Dropdown>
			<>
				<CheckPicker
					style={{
						float: "left",
						marginLeft: "10px",
						width: 224,
					}}
					label="Friends"
					data={data}
					disabled={disabled}
					valeu={authors}
					onChange={(e) => setAuthors(e)}
				/>
			</>

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
				Post
			</Button>
		</div>
	);
}

export default CREATEPOST;
