import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import PropTypes from 'prop-types';

class AnimatedButton extends Component {
	constructor(props) {
	super(props);
	this.state = {
	}
	}

	render() {
		const animatedButtonClasses = "ui basic animated circular button " + this.props.extraAttributes + " removeBorder"
		return (
			<div className={animatedButtonClasses} tabIndex="0" onClick={this.props.clickFunction}>
				<div className="visible content">
					{this.props.buttonText} 
				</div>
				<div className="hidden content"> <i className={this.props.iconForButton}> </i></div>					
			</div>
		)
	}
}

AnimatedButton.defaultProps = {
	clickFunction: () => {},
	extraAttributes: ""
}

AnimatedButton.propTypes = {
	iconForButton: PropTypes.string.isRequired,
	buttonText: PropTypes.string.isRequired,
	clickFunction: PropTypes.func,
};

export default AnimatedButton;