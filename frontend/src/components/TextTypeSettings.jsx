import React, { Component } from 'react'
import { Dropdown } from 'semantic-ui-react'
import './styles/TextTypeSettings.css';

const textTypeOptions = [
				{key: 'text/plain', text: 'Plain Text', value: 'text/plain'},
				{key: 'text/markdown', text: 'Markdown', value: 'text/markdown'},
				{key: 'application/base64', text: 'Base 64', value: 'application/base64'},			
				];


class TextTypeSettings extends Component {
	state = {key: 'text/plain', text: 'Plain Text', value: 'text/plain' };

	handleChange = (e, { value }) => {
		this.setState({ value });
		this.props.handleChange('textContentType', {value});
	}
	
	render() {
		const { value } = this.state
		return (
			<Dropdown 
				name='textContentType'
				onChange={this.handleChange}
				options={textTypeOptions}
				header='Text Type' 
				selection
				placeholder='Plain Text'
				value={value}
				className="dropDownBar"
			/>
		)
	}
}

export default TextTypeSettings