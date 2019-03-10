import React, { Component } from 'react';
import { Button, Modal, Dropdown, Icon } from 'semantic-ui-react';
import './styles/MultiInputModal.css';
import AnimatedButton from './AnimatedButton';

class MultiInputModal extends Component {
 		constructor(props) {
		super(props);
		this.state = {
			showModal: false,
			options: this.props.defaultValues, 
		};

		this.handleAddition = this.handleAddition.bind(this);
		this.clearSelection = this.clearSelection.bind(this);
		this.closeModal = this.closeModal.bind(this);
	}

	handleAddition = (e, { value }) => {
		this.setState({
			options: [{ text: value, value }, ...this.state.options],
		})
	}
	
	clearSelection() {
		this.setState({
			currentValues: [],
		})
	}

	closeModal() {
		if (this.state.currentValues) {
			this.props.handleCategoryChange(this.state.currentValues);
		}
		this.setState({
		 showModal: false 
		 });
	}

	handleChange = (e, { value }) => {
		this.setState({ currentValues: value });
	}
	
	render() {
		const { currentValues } = this.state;

		return (
			<Modal 
				trigger={<Button basic icon onClick={() => this.setState({showModal: true})} className="MultiInputModalButton"> <Icon name={this.props.icon}/> {this.props.buttonLabel} </Button>}
				open={this.state.showModal}
				onClose={this.closeModal}
			>
			<Modal.Header> Select Categories </Modal.Header>
			<Modal.Content>
			  <Dropdown
				options={this.state.options}
				placeholder={this.props.placeholder}
				search
				selection
				multiple
				allowAdditions
				closeOnChange={true}
				fluid
				value={currentValues}
				onAddItem={this.handleAddition}
				onChange={this.handleChange}
			  />
			</Modal.Content>
			<Modal.Actions>
			<AnimatedButton iconForButton="trash alternate outline icon" buttonText="Clear" clickFunction={this.clearSelection}/>
			<AnimatedButton iconForButton="checkmark icon" buttonText="Close" clickFunction={this.closeModal}/>
			</Modal.Actions>
			</Modal>
		)
	}
}

export default MultiInputModal