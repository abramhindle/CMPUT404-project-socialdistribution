import React, { Component } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getLeads, deleteLead } from '../../actions/leads';

export class Leads extends Component {
    static propTypes = {
        leads: PropTypes.array.isRequired,
        getLeads: PropTypes.func.isRequired,
        deleteLead: PropTypes.func.isRequired
    };

    componentDidMount() {
        this.props.getLeads();
    }

    render() {
        return (
            <div>
                <h1>Leads list</h1>
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Message</th>
                            <th />
                        </tr>
                    </thead>
                    <tbody>
                        { this.props.leads.map(lead => (
                            <tr key={lead.id}>
                                <td>{lead.id}</td>
                                <td>{lead.name}</td>
                                <td>{lead.email}</td>
                                <td>{lead.message}</td>
                                <td><button className="btn btn-danger btn-sm" onClick={this.props.deleteLead.bind(this, lead.id)}>Delete</button></td>
                            </tr>
                        )) }
                    </tbody>
                </table>
            </div>
        )
    }
}

// map state of redux to props of this component
const mapStateToProps = state => ({
    leads: state.leads.leads // reducers leads's leads
});

export default connect(mapStateToProps, { getLeads, deleteLead })(Leads);
