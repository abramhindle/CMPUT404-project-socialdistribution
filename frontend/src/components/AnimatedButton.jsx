import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';

class AnimatedButton extends Component {
	constructor(props) {
	super(props);
	this.state = {
	}
	}

	render() {
		return (
			<div className="ui basic animated circular button removeBorder" tabIndex="0">
				<div className="visible content">
					<i className={this.props.iconForButton}> </i>
				</div>
				<div className="hidden content"> {this.props.buttonText} </div>					
			</div>
		)
	}
}

export default AnimatedButton;