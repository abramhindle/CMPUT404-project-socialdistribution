import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import SideBar from '../components/SideBar';
import PostInput from '../components/PostInput';

import {connect} from 'react-redux';

import {notes} from "../actions";

class Stream extends Component {	

    componentDidMount() {
        this.props.fetchNotes();
    }

	constructor(props) {
		super(props);
		this.state = {
		}
	}	

	render() {
	return(
		  <div>		
			<SideBar/>
			<div className="pusher">
				<h1> This is where we put the stuff for the current page</h1>
				<PostInput/>
			</div>
		  </div>
	    )
    }
}

const mapStateToProps = state => {
    return {
        notes: state.notes,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        fetchNotes: () => {
            dispatch(notes.fetchNotes());
        }
    }
}


export default connect(mapStateToProps, mapDispatchToProps)(Stream);
