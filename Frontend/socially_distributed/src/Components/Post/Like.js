import React, { useState, useEffect } from "react";
import { Avatar, Panel } from "rsuite";
// Component Imports

function LIKE({ likeobj }) {
	const [like, set_like] = useState(likeobj);

	return (
		<Panel bordered style={{ marginBottom: "5px" }}>
			<Avatar
				style={{ float: "left" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			></Avatar>
			<h3>{like["summary"]}</h3>
		</Panel>
	);
}

export default LIKE;
