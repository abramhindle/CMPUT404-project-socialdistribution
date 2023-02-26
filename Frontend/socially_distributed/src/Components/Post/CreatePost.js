import React, { useState } from "react";
import { Input, Avatar, Panel, Dropdown, Uploader } from "rsuite";
// import { Scrollbars } from "react-custom-scrollbars-2";
// Component Imports

function CREATEPOST() {
	const [post_status, set_post_status] = useState("Public");
	const [post_type, set_post_type] = useState("Text");

	const input = () => {
		if (post_type === "Text") {
			return (
				<Input
					style={{ float: "left", marginTop: "5px" }}
					as="textarea"
					rows={5}
					placeholder="Text"
				/>
			);
		}

		if (post_type === "Image") {
			return (
				<Uploader
					action="//jsonplaceholder.typicode.com/posts/"
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
						<span>Click or Drag files to this area to upload</span>
					</div>
				</Uploader>
			);
		}
	};

	return (
		<div
			style={{
				marginBottom: "5px",
				display: "block",
				height: "25vh",
				border: "1px solid black",
				borderRadius: "10px",
				padding: "5px",
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
			{input()}
		</div>
	);
}

export default CREATEPOST;
