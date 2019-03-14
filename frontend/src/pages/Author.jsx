import React, { Component } from 'react';
import 'semantic-ui-css/semantic.min.css';
import HTTPFetchUtil from "../util/HTTPFetchUtil";
import AuthorViewComponent from "../components/AuthorViewComponent";

class Author extends Component {	

    constructor(props) {
		super(props);
		this.state = {
            bio: "",
            displayName: "",
            email: "",
            firstName: "",
            github: "",
            host: "",
            id: "",
            url: "",
            lastName: "",
		}
    } 

    componentDidMount(){
        let hostUrl = "/api/author/"+this.props.match.params.authorId
        let requireAuth = true
        let returnHTTP = HTTPFetchUtil.getRequest(hostUrl, requireAuth)
            .then((httpResponse) => {
                if (httpResponse.status === 200) {
                    httpResponse.json().then((results) => {
                        this.setState({
                            bio: results.bio,
                            displayName: results.displayName,
                            email: results.email,
                            firstName: results.firstName,
                            github: results.github,
                            host: results.host,
                            id: results.id,
                            url: results.url,
                            lastName: results.lastName,
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }

	render() {
        return(	
            <div className="pusher">
                <AuthorViewComponent data={this.state}/>
            </div>
        )
    }
}



export default Author;