import React, { Component } from 'react';
import { Button, Modal, Dropdown, Icon } from 'semantic-ui-react';
import './styles/CategoriesModal.css';
import AnimatedButton from './AnimatedButton';
import HTTPFetchUtil from '../util/HTTPFetchUtil.js';

function createCategoriesItem(responseItem) {
	var categoryName = responseItem.name;
	return({ key: categoryName, text: categoryName, value: categoryName});
}

class CategoriesModal extends Component {
 		constructor(props) {
		super(props);
		this.state = {
			showModal: false,
			options: [],
			isFetching: false,
		};
		
		this.getCategories = this.getCategories.bind(this);
		this.handleAddition = this.handleAddition.bind(this);
		this.clearSelection = this.clearSelection.bind(this);
		this.closeModal = this.closeModal.bind(this);
		
	}
	
	componentDidMount() {
		this.getCategories();
	}

	getCategories() {
		this.setState({ isFetching: true });
		const requireAuth = true, urlPath = "/api/categories/";
			HTTPFetchUtil.getRequest(urlPath, requireAuth)
			.then((httpResponse) => {
				console.log(httpResponse);
				if(httpResponse.status === 200) {
					httpResponse.json().then((results) => {	
					this.setState({
						options: results.map(createCategoriesItem),
						isFetching: false,
						});
					})
				}
				else {
					this.setState({
							options: [{ key: 'School', text: 'School', value: 'School' },
									{ key: 'YEG', text: 'YEG', value: 'YEG' },
									{ key: 'OOTD', text: 'OOTD', value: 'OOTD' },],
							isFetching: false,
							});
				}
			})
			.catch((error) => {
				console.error(error, "ERROR");
			});
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
		const { currentValues, isFetching } = this.state;

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
				disabled={isFetching}
				loading={isFetching}
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