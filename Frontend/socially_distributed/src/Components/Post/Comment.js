import React, { useState, useEffect } from "react";
import { Input, InputGroup, Panel } from "rsuite";
import { Scrollbars } from "react-custom-scrollbars-2";
// Component Imports

function COMMENTS({ postobj }) {
	const [comments, set_comments] = useState(
		postobj["commentsSrc"]["comments"]
	);
	const [comment, set_comment] = useState("");

	return (
		<div
			style={{
				display: "block",
				height: "50vh",
				borderLeft: "2px solid black",
				padding: "10px",
			}}
		>
			<h4>Commnets</h4>
			{comments.map((obj) => (
				<div>
					<h5
						style={{
							marginLeft: "10px",
							float: "left",
						}}
					>
						{obj["author"]["displayName"]}
					</h5>
					<p>{obj["comment"]}</p>
				</div>
			))}

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

export default COMMENTS;
