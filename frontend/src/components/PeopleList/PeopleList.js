import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';

import Person from './Person/Person';

import InputBase from '@material-ui/core/InputBase';
import { remove } from 'lodash';

const useStyles = makeStyles(() => ({
	root: {
		backgroundColor: "white",
		marginBottom: "30px",
		borderRadius: '10px',
		paddingBottom: '0.5em',
		boxShadow: '2px 2px 4px'
	},
	title: {
		fontWeight: 'bold'
	},
	container: {
		display: 'flex',
		padding: '0.5em 0.5em'
	},
	controls: {
		marginLeft: 'auto'
	},
	control: {
		marginLeft: '0.5em',
		borderRadius: '20px',
		width: '30px',
		'&:hover': {
            backgroundColor: '#D3D3D3',
        }
	},
	active: {
		backgroundColor: 'gray',
		'&:hover': {
            backgroundColor: 'gray',
        }
	},
	textField: {
		marginLeft: '0.5em',
		marginRight: '0.5em',
		border: '1px solid black',
		width: '-webkit-fill-available',
		padding: '0em 0.5em',
		borderRadius: '5px'
	},
	peopleList: {
		maxHeight: '10em',
		overflow: 'scroll'
	}
}));

export default function PeopleList(props) {
	const classes = useStyles();
	
	const [addFriend, setAddFriend] = useState(false);
	const [removeFriend, setRemoveFriend] = useState(false);
	const [people, setPeople] = useState(props.people.map((d, i) => <Person key={i} friend={d} addClicked={addPersonClicked}/>));
	let searchText = '';

	const updatePeople = (type) => {
		let data = null;
		let showButton = false;
		let isDelete = false;

		switch (type) {
			case 'friends':
				data = props.people;
				break;
			case 'search':
				data = _.filter(props.all_authors, d => d.displayName.includes(searchText));
				showButton = true;
				break;
			case 'remove_friends':
				isDelete = true;
				data = props.people;
				showButton = true;
				break;
			default:
				break;
		}
		if (data) {
			setPeople(data.map((d, i) => <Person key={i} friend={d} showButton={showButton} isDelete={isDelete} followed={_.findIndex(props.followers, follower => follower.id === d.id) === -1} addClicked={addPersonClicked}/>));
		}
	}

	const addFriendClicked = () => {
		setAddFriend(!addFriend);
		if (removeFriend) {
			setRemoveFriend(!removeFriend);
		}
		if (addFriend) {
			updatePeople('friends');
		} else {
			updatePeople('search');
		}
	}

	const removeFriendClicked = () => {
		setRemoveFriend(!removeFriend);
		if (addFriend) {
			setAddFriend(!addFriend);
		}
		if (!removeFriend) {
			updatePeople('remove_friends');
		}
	}

	const onTextChange = (e) => {
		searchText = e.target.value;
		updatePeople('search');
	}

	const addPersonClicked = (person, isDelete) => {
		if (!isDelete) {
			const object = person;
			const post = {
				type: 'Follow',
				summary: `${props.author.displayName} wants to follow ${object.displayName}`,
				actor: props.author,
				object
			}
			props.postFriendRequest(post, object);
		} else {
			props.unfriend(person);
		}
	}

	let searchBar = addFriend
		? <InputBase
				className={classes.textField}
				onChange={onTextChange}
				placeholder='Search for someone'
				id='textTags'
			/>
		: null;

	React.useEffect(() => {
		if (addFriend) {
			updatePeople('search');
		} else {
			updatePeople('friends');
		}
	}, [props.all_authors, props.people]);	

	return (
		<div className={classes.root}>
			<div className={classes.container}>
				<div>
					<span className={classes.title}>{props.title}</span>
				</div>
				{ !props.static ? <div className={classes.controls}>
					<svg
						className={addFriend ? [classes.control, classes.active].join(' ') : classes.control}
						onClick={addFriendClicked}
						id='addFriend'
						width="21"
						height="21"
						viewBox="0 0 21 21"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<g clipPath="url(#clip0)">
							<path d="M14 18.375V16.625C14 15.6967 13.6313 14.8065 12.9749 14.1501C12.3185 13.4937 11.4283 13.125 10.5 13.125H4.375C3.44674 13.125 2.5565 13.4937 1.90013 14.1501C1.24375 14.8065 0.875 15.6967 0.875 16.625V18.375" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
							<path d="M7.4375 9.625C9.3705 9.625 10.9375 8.058 10.9375 6.125C10.9375 4.192 9.3705 2.625 7.4375 2.625C5.5045 2.625 3.9375 4.192 3.9375 6.125C3.9375 8.058 5.5045 9.625 7.4375 9.625Z" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
							<path d="M17.5 7V12.25" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
							<path d="M20.125 9.625H14.875" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
						</g>
						<defs>
							<clipPath id="clip0">
								<rect width="21" height="21" fill="white"/>
							</clipPath>
						</defs>
					</svg>
					<svg
						className={removeFriend ? [classes.control, classes.active].join(' ') : classes.control}
						onClick={removeFriendClicked}
						id='removeFriend'
						width="21"
						height="21"
						viewBox="0 0 21 21"
						fill="none"
						xmlns="http://www.w3.org/2000/svg"
					>
						<g clipPath="url(#clip0)">
							<path d="M14 18.375V16.625C14 15.6967 13.6313 14.8065 12.9749 14.1501C12.3185 13.4937 11.4283 13.125 10.5 13.125H4.375C3.44674 13.125 2.5565 13.4937 1.90013 14.1501C1.24375 14.8065 0.875 15.6967 0.875 16.625V18.375" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
							<path d="M7.4375 9.625C9.3705 9.625 10.9375 8.058 10.9375 6.125C10.9375 4.192 9.3705 2.625 7.4375 2.625C5.5045 2.625 3.9375 4.192 3.9375 6.125C3.9375 8.058 5.5045 9.625 7.4375 9.625Z" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
							<path d="M15.75 7L20.125 11.375" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
							<path d="M20.125 7L15.75 11.375" stroke="#25282B" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
						</g>
						<defs>
							<clipPath id="clip0">
								<rect width="21" height="21" fill="white"/>
							</clipPath>
						</defs>
					</svg>
				</div> : null}
			</div>
			{ searchBar }
			<div className={classes.peopleList}>
				{ people }
			</div>
		</div>
	)
}
