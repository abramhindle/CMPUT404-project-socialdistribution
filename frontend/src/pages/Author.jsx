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
            hostUrl: "",
		}
		this.fetchProfile = this.fetchProfile.bind(this);
    }

    fetchProfile() {
        let hostUrl = "/api/author/"+ this.props.match.params.authorId //"df57cce0-8eae-44d9-8f43-8033e099b917" //this.props.match.params.authorId
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
                            hostUrl: hostUrl,
                        })
                    })
                }
            })
            .catch((error) => {
                console.error(error);
        });
    }

    componentDidMount(){
        this.fetchProfile();
    }

	render() {
        return(	
            <div className="pusher">
                <AuthorViewComponent
                    profile_id={this.state.id}
                    host={this.state.host}
                    displayName={this.state.displayName}
                    url={this.state.url}
                    github={this.state.github}
                    firstName={this.state.firstName}
                    lastName={this.state.lastName}
                    email={this.state.email}
                    bio={this.state.bio}
                    onSuccess={this.fetchProfile}
                    hostURL={this.state.hostUrl}
                />
            </div>
        )
    }
}



export default Author;