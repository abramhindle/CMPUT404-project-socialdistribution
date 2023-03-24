import React, { useState } from "react";
import { Button, Avatar, Panel, useToaster, Message } from "rsuite";
import { reqInstance } from "../utils/axios";
import { getAuthorId } from "../utils/auth";
import PROFILEIMAGE from "../Profile/ProfileImage";

function FOLLOWREQ({ obj }) {
	const [follow, setFollow] = useState(obj);
	const toaster = useToaster();

	async function acceptFriend() {
		const curr_author_id = getAuthorId(null);
		var FAID = getAuthorId(obj.actor.id);
		const url2 = obj;

		const params = {};
		const url = `authors/${curr_author_id}/followers/${FAID}/`;

		reqInstance({ method: "put", url: url, data: params })
			.then((res) => {
				toaster.push(
					<Message type="success">
						{res.data.displayName} now follows you
					</Message>,
					{
						placement: "topEnd",
						duration: 5000,
					}
				);
			})
			.catch((err) => {
				toaster.push(<Message type="error">{err}</Message>, {
					placement: "topEnd",
					duration: 5000,
				});
			});
	}

	return (
		<Panel
			bordered
			style={{
				marginBottom: "5px",
			}}
		>
			<div>
				<Avatar
					style={{ float: "left", marginBotton: "5px" }}
					circle
					src={follow["actor"]["profileImage"]} //{follow[actor][profileImage]} replace this with the actors profile image url
				/>
				<div
					style={{
						marginLeft: "50px",
						fontFamily: "Times New Roman",
						fontWeight: "bold",
						fontSize: "20px",
					}}
				>
					{follow["summary"]}
				</div>
			</div>

			<div style={{ marginTop: "10px" }}>
				<Button block onClick={acceptFriend} appearance="primary">
					Accept
				</Button>
				<Button block>Deny</Button>
			</div>
		</Panel>
	);
}

export default FOLLOWREQ;
