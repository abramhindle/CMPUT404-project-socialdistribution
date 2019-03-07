import React, { Component } from 'react'
import { Dropdown } from 'semantic-ui-react'
import './styles/VisibilitySettings.css';

const visibilityOptions = [
						{key: 'PUBLIC', text: 'PUBLIC', value: 'PUBLIC'},
						{key: 'FRIENDS', text: 'FRIENDS', value: 'FRIENDS'},
						{key: 'FOAF', text: 'FOAF', value: 'FOAF'},
						{key: 'SERVERONLY', text: 'SERVERONLY', value: 'SERVERONLY'},
						{key: 'PRIVATE', text: 'PRIVATE', value: 'PRIVATE'}
						];


class VisibilitySettings extends Component {
	state = {key: 'PUBLIC', text: 'PUBLIC', value: 'PUBLIC'};
	
	handleChange = (e, { value }) => {
		this.setState({ value });
		this.props.handleChange('visibility', {value});
	}
	
	render() {
		const { value } = this.state;
    
		return (
			<Dropdown
				name="visibility"
				onChange={this.handleChange}
				options={visibilityOptions}
				header="Visible To"
				selection
				placeholder="PUBLIC"
				value={value}
				className="dropDownBar"
			/>
		)
	}
}

export default VisibilitySettings;