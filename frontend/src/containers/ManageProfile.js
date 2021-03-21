import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import ProfileInfo from '../components/ProfileInfo/ProfileInfo';
import Navbar from '../components/Navbar/Navbar';

const useStyles = makeStyles(() => ({
    root: {
        backgroundColor: "#EFEFEF",
        height: "100vh"
    },
    container: {
        padding: '0px 10%'
    },
    manageProfileForm: {
        padding: "1em",
        backgroundColor: "white",
        width: "50%",
        height: "500px",
        borderRadius: "8px"
    },
    profileSetting: {
        display: "flex",
        justifyContent: "space-between",
        margin: "1em",
    }
  }));


function ManageProfile(props) {
    const classes = useStyles();

    const container = ['container-fluid', classes.container];

    const temp_profile = {
        type: 'author',
        id: 'http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e',
        host: 'http://127.0.0.1:5454/',
        displayName: 'Lara Croft',
        url:'http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e',
        github: 'http://github.com/laracroft'
    };

    return (
        <div 
            className={classes.root}
        >
            <Navbar />
            <div className={container.join(' ')}>
                <div className='row align-items-start' >
                 
                    <div className={classes.manageProfileForm}>
                        <h2>Manage Profile</h2>

                        <hr></hr>

                        <div className={classes.profileSetting}>
                            <span>Display Name: { temp_profile.displayName }</span><span>Edit</span>
                        </div>
                       
                        <div className={classes.profileSetting}>
                            <span>GitHub URL: { temp_profile.github }</span><span>Edit</span>            
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}

const mapStateToProps = (state) => ({
    author: state.users.user
});
  
export default ManageProfile;