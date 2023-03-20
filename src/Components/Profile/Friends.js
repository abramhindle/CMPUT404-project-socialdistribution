import React, { useLayoutEffect, useState } from "react";
import { Avatar } from "rsuite";
import axios from "axios";
import { getAuthorId } from "../utils/auth";
import { useNavigate } from "react-router-dom";
import PROFILEIMAGE from "./ProfileImage";

function FRIENDS() {
	const [friends, setFriends] = useState({ items: [] });
	let navigate = useNavigate();

	useLayoutEffect(() => {
		if (!localStorage.getItem("loggedIn")) {
			navigate("/login");
		} else {
			const AUTHOR_ID = getAuthorId(null);
			const url = `authors/${AUTHOR_ID}/followers/`;
			axios({
				method: "get",
				url: url,
			}).then((res) => {
				setFriends(res.data);
			});
		}
	}, []);

	const item = (obj) => {
		return (
			<div
				key={obj.id}
				style={{
					height: "50px",
					border: "0.5px solid lightgrey",
					borderRadius: "10px",
					marginTop: "5px",
				}}
			>
				<div style={{ padding: "5px" }}>
					<Avatar
						style={{ float: "left", marginBotton: "5px" }}
						circle
						src={obj["profileImage"]} //{follow[actor][profileImage]} replace this with the actors profile image url
					/>
					<h5
						style={{
							marginLeft: "10px",
							float: "left",
						}}
					>
						{obj["displayName"]}
					</h5>
				</div>
			</div>
		);
	};

	return <div>{friends.items.map((obj) => item(obj))}</div>;
}

export default FRIENDS;
