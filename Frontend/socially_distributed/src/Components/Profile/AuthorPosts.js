import React, { useState } from "react";
import { Panel, PanelGroup } from "rsuite";
import COMMENTS from "../Post/Comment";

function AUTHORPOSTS() {
	// make a get request to get author and every post the author made and comments on the posts
	// make a get request to get all the friends of an author
	const posts = {
		type: "inbox",
		author: "http://127.0.0.1:5454/authors/c1e3db8ccea4541a0f3d7e5c75feb3fb",
		items: [
			{
				type: "post",
				title: "A Friendly post title about a post about web dev",
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/764efa883dda1e11db47671c4a3bbd9e",
				source: "http://lastplaceigotthisfrom.com/posts/yyyyy",
				origin: "http://whereitcamefrom.com/posts/zzzzz",
				description: "This post discusses stuff -- brief",
				contentType: "text/plain",
				content:
					"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
				author: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					host: "http://127.0.0.1:5454/",
					displayName: "Lara Croft",
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					github: "http://github.com/laracroft",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				categories: ["web", "tutorial"],
				comments:
					"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
				published: "2015-03-09T13:07:04+00:00",
				visibility: "FRIENDS",
				unlisted: false,
			},
			{
				type: "post",
				title: "DID YOU READ MY POST YET?",
				id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/999999983dda1e11db47671c4a3bbd9e",
				source: "http://lastplaceigotthisfrom.com/posts/yyyyy",
				origin: "http://whereitcamefrom.com/posts/zzzzz",
				description: "Whatever",
				contentType: "text/plain",
				content: "Are you even reading my posts Arjun?",
				author: {
					type: "author",
					id: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					host: "http://127.0.0.1:5454/",
					displayName: "Lara Croft",
					url: "http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
					github: "http://github.com/laracroft",
					profileImage: "https://i.imgur.com/k7XVwpB.jpeg",
				},
				categories: ["web", "tutorial"],
				comments:
					"http://127.0.0.1:5454/authors/9de17f29c12e8f97bcbbd34cc908f1baba40658e/posts/de305d54-75b4-431b-adb2-eb6b9e546013/comments",
				published: "2015-03-09T13:07:04+00:00",
				visibility: "FRIENDS",
				unlisted: false,
			},
		],
	};

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
				header={obj["title"]}
				style={{
					// height: "50px",
					// border: "0.5px solid lightgrey",
					// borderRadius: "10px",
					marginTop: "5px",
				}}
				bordered
				collapsible
			>
				<div style={{ padding: "5px" }}>
					<h3
						style={{
							marginLeft: "10px",
							float: "left",
						}}
					>
						{obj["description"]}
					</h3>
					<br />
					<p>{body(obj)}</p>
				</div>
				<Panel bordered collapsible header="Comments">
					<COMMENTS postobj={obj}></COMMENTS>
				</Panel>
			</Panel>
		);
	};

	return <PanelGroup>{posts.items.map((obj) => item(obj))}</PanelGroup>;
}

export default AUTHORPOSTS;
