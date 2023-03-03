import React, { useState, useEffect } from "react";
import { Avatar, Panel } from "rsuite";
// Component Imports

function LIKE({ likeobj }) {
	const [like, set_like] = useState(likeobj);

	return (
		<Panel bordered style={{ marginBottom: "5px" }}>
			<Avatar
				style={{ float: "left", marginBotton: "5px" }}
				circle
				src="https://avatars.githubusercontent.com/u/12592949"
			></Avatar>
			<h4 style={{ marginLeft: "50px" }}>{like["summary"]}</h4>
		</Panel>
	);
}

export default LIKE;
