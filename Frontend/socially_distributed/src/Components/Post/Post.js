import React, { useState } from "react";
import { Input, Avatar, InputGroup, Panel } from "rsuite";
import { Scrollbars } from "react-custom-scrollbars-2";
// Component Imports

function POST({ postobj }) {
	const [post, set_post] = useState(postobj);
	const [comment, set_comment] = useState("");

	const body = () => {
		if (post["contentType"] === "text/plain") {
			return <p>{post["content"]}</p>;
		}
		
		// Peter you just need to return the image here 
		if (post["contentType"] === "image/jpeg") {
			return <div>image</div>;
		}
	};

	return (
		<div
			style={{
				display: "block",
				height: "50vh",
				borderTop: "2px solid grey",
				width: "50%",
				margin: "auto",
			}}
		>
			<div
				style={{
					padding: "5px",
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
						paddingTop: "5px",
						marginLeft: "10px",
						float: "left",
					}}
				>
					{post["author"]["displayName"]}
				</h5>
			</div>
			<Scrollbars style={{ height: "320px" }}>
				<div>
					<h3>{post["title"]}</h3>
					<h5>{post["description"]}</h5>
					<p style={{ padding: "5px" }}>{body()}</p>
				</div>
			</Scrollbars>
			<InputGroup inside>
				<Input
					onChange={(e) => set_comment(e)}
					value={comment}
					placeholder="comment"
				/>
				<InputGroup.Button>Submit</InputGroup.Button>
			</InputGroup>
		</div>
	);
}

export default POST;
