import React, { useEffect, useLayoutEffect, useState } from "react";
import { Panel, PanelGroup } from "rsuite";
import COMMENTS from "../Post/Comment";
import axios from "axios";
import { useParams } from "react-router-dom";
import POST from "../Post/Post";
import { getAuthorId } from "../utils/auth";
import { useNavigate } from "react-router-dom";

function AUTHORPOSTS() {
	const [posts, setPosts] = useState([]);
	let navigate = useNavigate();

	useEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/login");
		} else {
			const author_id = getAuthorId();
			const url = `posts/authors/${author_id}/posts/`;
			axios({ method: "get", url: url })
				.then((res) => {
					console.log(res.data);
					setPosts(res.data.results);
				})
				.catch((err) => console.log(err));
		}
	}, []);

	const body = (obj) => {
		if (obj["contentType"] === "text/plain") {
			return <p style={{ padding: "5px" }}>{obj["content"]}</p>;
		}

		// Peter you just need to return the image here
		if (obj["contentType"] === "image/jpeg") {
			return <div>image</div>;
		}
	};

	const item = (obj) => {
		return (
			<Panel
				header={<div>{obj["title"]}</div>}
				style={{
					marginTop: "5px",
				}}
				bordered
				collapsible
			>
				<POST postobj={obj}></POST>
			</Panel>
		);
	};

	return <PanelGroup>{posts.map((obj) => item(obj))}</PanelGroup>;
}

export default AUTHORPOSTS;
