import React, { Component } from 'react';
import { Input } from 'semantic-ui-react'
import './PostInput.css';

class PostInput extends Component {	

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	return(
		  <div class="PostInputBoxPosition">
			<div>
            <Input placeholder='What are you thinking about today...?' />
			<button class="ui button"> POST </button>
        	<button class="ui button"> IMG </button>  
			</div>
		</div>
	)
}
}

export default PostInput;