import React, { useState, useEffect } from "react";
import { Avatar } from "rsuite";
// Component Imports

function LIKE({ likeobj }) {
	const [like, set_like] = useState(likeobj);

	return (
		<div
			style={{
				border: "1px solid black",
				borderRadius: "10px",
				marginBottom: "5px",
			}}
		>
			<Avatar
				style={{ float: "left" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			></Avatar>
			<h3>{like["summary"]}</h3>
		</div>
	);
}

export default LIKE;
