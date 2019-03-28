import React, { Component } from 'react';
import { Dropdown, Modal } from 'semantic-ui-react';
import AnimatedButton from './AnimatedButton';
import './styles/VisibilitySettings.css';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';
import AbortController from 'abort-controller';
import PropTypes from 'prop-types';
import { toast } from 'react-semantic-toasts';
import 'react-semantic-toasts/styles/react-semantic-alert.css';

const controller = new AbortController();
const signal = controller.signal;
signal.addEventListener("abort", () => {});

function createFriendItem(responseItem) {
	const friendName = responseItem.displayName;
	const friendID = responseItem.id;
	return({ key: friendName, text: friendName, value: friendID});
}


class VisibilitySettings extends Component {
	constructor(props) {
		super(props);
		this.state = {
			multiple: true,
			search: true,
			searchQuery: null,
			value: [],
			options: [],
			visibility: this.props.visibility,
			open: false,
			showModal: false,
		};
		this.getMyFriends = this.getMyFriends.bind(this);
		this.clearSelection = this.clearSelection.bind(this);

	}
	
	componentDidMount() {
		this.getMyFriends();
	}
	
	componentWillUnmount() {
		controller.abort();
	}

	getMyFriends() {
		var UUID = this.props.userID;	
		const requireAuth = true,
			urlPath = '/api/author/' + UUID;
			HTTPFetchUtil.getRequest(urlPath, requireAuth, signal)
			.then((httpResponse) => {
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {
						this.setState({
							options: results.friends.map(createFriendItem), 
						});
					})
				}
				else {
					toast(
						{
							type: 'error',
							icon: 'window close',
							title: 'Failed',
							description: <p> Failed to fetch friends. </p>,
						}
					);
				}
			})
			.catch((error) => {
				console.error(error);
			});
	}
	
	
	clearSelection() {
		this.setState({
			value: [],
		});
		this.props.handleChange('visibleTo', {});
	}
	
	
	openCloseDropdown = () => {
		if (this.state.showModal === false) {
			this.setState({
				open: !this.state.open,
			});
		}
	}
	
	handleVisibilityChange = (e, { value }) => {
		this.setState({ visibility: value });
		this.props.handleChange('visibility', {value});
	}

	handleChange = (e, { value }) => {
		this.setState({ value });
		this.props.handleChange('visibleTo', {value});
	}
		
	handleSearchChange = (e, { searchQuery }) => this.setState({ searchQuery })
	
	closeModal = () => {
		this.setState({
			showModal: false, 
			visibility: 'PRIVATE',
			});
		this.props.handleChange('visibility', {value: 'PRIVATE'});
	}
	
	render() {
		const { multiple, options, search, value} = this.state;

		return (
			<Dropdown text={this.state.visibility} open={this.state.open} onClick={this.openCloseDropdown} labeled button className='dropDownBar'>
				<Dropdown.Menu open={this.state.open}>
					<Dropdown.Header icon='tags' content='Visible To' />
					<Dropdown.Divider />
					<Dropdown.Item text='PUBLIC' value="PUBLIC" onClick={this.handleVisibilityChange}/>
					<Dropdown.Item text='FRIENDS' value="FRIENDS" onClick={this.handleVisibilityChange}/>
					<Dropdown.Item text='FOAF' value="FOAF" onClick={this.handleVisibilityChange}/>
					<Dropdown.Item text='SERVERONLY' value="SERVERONLY" onClick={this.handleVisibilityChange}/>
					<Dropdown.Item text='PRIVATE' value="PRIVATE" onClick={ () => this.setState({showModal: true, open: false})}/>
				
					<Modal 
					open={this.state.showModal}
					onClose={this.closeModal}
					>
					<Modal.Header> This post will be visible to you and... </Modal.Header>
						<Modal.Content>
							<Dropdown
								fluid
								selection
								multiple={multiple}
								closeOnChange={true}
								search={search}
								options={options}
								value={value}
								placeholder='Add Users'
								onChange={this.handleChange}
								onSearchChange={this.handleSearchChange}
							/>
						</Modal.Content>
						<Modal.Actions>
							<AnimatedButton iconForButton="trash alternate outline icon" buttonText="CLEAR" clickFunction={this.clearSelection} extraAttributes={"negative"}/>
							<AnimatedButton iconForButton="checkmark icon" buttonText="DONE" clickFunction={this.closeModal} extraAttributes={"positive"}/>
						</Modal.Actions>
					</Modal>
				</Dropdown.Menu>
			</Dropdown>
		)
	}
}

VisibilitySettings.defaultProps = {
	visibility: "PUBLIC",
};

VisibilitySettings.propTypes = {
	visibility: PropTypes.string,
	userID: PropTypes.string.isRequired, 
	handleChange: PropTypes.func.isRequired,
};

export default VisibilitySettings;