import React, { useEffect, useState } from "react";
import { Button, Input, Panel, InputGroup, Message, useToaster } from "rsuite";
import EyeIcon from "@rsuite/icons/legacy/Eye";
import EyeSlashIcon from "@rsuite/icons/legacy/EyeSlash";
import axios from "axios";
import {
	getCsrfToken,
	setCurrentUser,
	setLoggedIn,
	unsetCurrentUser,
	setCreds,
} from "../utils/auth";
import { useNavigate } from "react-router-dom";

function LOGIN() {
	const [username, set_username] = useState("");
	const [password, set_password] = useState("");
	const [visible, setVisible] = React.useState(false);
	let toaster = useToaster();
	let navigate = useNavigate();

	useEffect(() => {
		if (localStorage.getItem("loggedIn")) {
			navigate("/");
		} else {
			unsetCurrentUser();
			getCsrfToken();
		}
	}, []);

	const handleChange = () => {
		setVisible(!visible);
	};

	const notifyFailedPost = (error) => {
		toaster.push(<Message type="error">{error}</Message>, {
			placement: "topEnd",
			duration: 5000,
		});
	};

	function delay(time) {
		return new Promise((resolve) => setTimeout(resolve, time));
	}

	delay(1000).then(() => console.log("ran after 1 second1 passed"));

	async function handleLoginClick() {
		var params = {
			username: username,
			password: password,
		};
		await getCsrfToken();
		const token = localStorage.getItem("token");

		let reqInstance = axios.create({
			headers: { "X-CSRFToken": token },
			baseURL: `http://127.0.0.1:8000/`,
		});
		reqInstance({ method: "post", url: "dlogin", data: params })
			.then(async (res) => {
				getCsrfToken();
				setLoggedIn(true);
				setCreds(params);
				await setCurrentUser(res.data).then(navigate("/"));
			})
			.catch((err) => notifyFailedPost(err.response.data));
	}

	return (
		<div>
			<Panel header="Login" shaded style={{ textAlign: "center" }}>
				<Input
					onChange={(e) => set_username(e)}
					value={username}
					placeholder="username"
					style={{ width: "70%", margin: "auto" }}
				/>
				<InputGroup
					inside
					style={{ width: "70%", margin: "auto", marginTop: "10px" }}
				>
					<Input
						onChange={(e) => set_password(e)}
						value={password}
						placeholder="password"
						type={visible ? "text" : "password"}
					/>
					<InputGroup.Button onClick={handleChange}>
						{visible ? <EyeIcon /> : <EyeSlashIcon />}
					</InputGroup.Button>
				</InputGroup>
				<Button
					apperance="Primary"
					block
					style={{ width: "70%", margin: "auto", marginTop: 10 }}
					onClick={handleLoginClick}
				>
					Login
				</Button>
			</Panel>
		</div>
	);
}

export default LOGIN;
