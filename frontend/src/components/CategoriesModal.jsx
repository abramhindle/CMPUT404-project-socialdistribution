import React, { Component } from 'react';
import { Button, Modal, Dropdown, Icon } from 'semantic-ui-react';
import './styles/CategoriesModal.css';
import AnimatedButton from './AnimatedButton';

function getCategories() {
//	const requireAuth = true,
//		urlPath = "/api/categories/".format(self.userID),
//		HTTPFetchUtil.getRequest(urlPath, requireAuth)
//		.then((httpResponse) => {
//			if(httpResponse.status === 200) {
//				httpResponse.json().then((results) => {
//				console.log(results);				
//				return(results);
//				})
//			}
//		})
//		.catch((error) => {
//		console.error(error);
//		});

	return [{ key: 'School', text: 'School', value: 'School' },
								{ key: 'YEG', text: 'YEG', value: 'YEG' },
								{ key: 'OOTD', text: 'OOTD', value: 'OOTD' },];
}


class CategoriesModal extends Component {
 		constructor(props) {
		super(props);
		this.state = {
			showModal: false,
			options: [],
		};

		this.handleAddition = this.handleAddition.bind(this);
		this.clearSelection = this.clearSelection.bind(this);
		this.closeModal = this.closeModal.bind(this);
	}

	componentWillMount() {
		this.setState({
			options: getCategories(),
		})
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
				trigger={<Button basic icon onClick={() => this.setState({showModal: true})} className="CategoriesModalButton"> <Icon name={"list alternate"}/> {"Categories"} </Button>}
				open={this.state.showModal}
				onClose={this.closeModal}
			>
			<Modal.Header> Select Categories </Modal.Header>
			<Modal.Content>
			  <Dropdown
				options={this.state.options}
				placeholder={"Add or Select Categories"}
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

export default CategoriesModal