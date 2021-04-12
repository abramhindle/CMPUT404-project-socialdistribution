import React from 'react';
import { useHistory } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
// import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(() => ({
    root: {
        flexGrow: 1,
        backgroundColor: "#FFF",
        marginBottom: "30px"
    },
    container: {
        display: 'flex'
    },
    logo: {
        height: '45px',
        width: '45px',
        backgroundColor: '#D1305E',
        borderRadius: '10px',
        marginLeft: '10%'
    },
    icon: {
        height: '45px',
        width: '45px',
        backgroundColor: '#D1305E',
        borderRadius: '100px',
        marginLeft: '10%',
        left: '70%'
    },
    logoutText: {
        color: 'black'
    },
    logout: {
        textAlign: 'center',
        flex: '0 0 auto',
        width: '5%',
        '&:hover': {
            backgroundColor: '#FFCCCB',
        }
    }
}));

export default function Navbar() {
    const classes = useStyles();
    const history = useHistory();
    
    const onIconClick = (e) => {
        history.push("/profile");
    };

    const onHomepageClick = (e) => {
        history.push("/feed");
    }

    function deleteAllCookies() {
        var cookies = document.cookie.split(";");
    
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i];
            var eqPos = cookie.indexOf("=");
            var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
            document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
        }
    }
    
    const onLogoutClicked = () => {
        deleteAllCookies();
        window.location.reload();
    }

    return (
        <AppBar
            className={classes.root}
            position="static"
            elevation={0}
        >
            <Toolbar >
                <div className='container-fluid'>
                    <div className='row align-items-start'>
                        <div className={'col-8'}>
                            <div className={classes.logo} onClick={onHomepageClick}></div>
                        </div>
                        <div className={'col-3'}>
                            <div
                                className={classes.icon}
                                onClick={onIconClick}
                            ></div>
                        </div>
                        <div className={classes.logout} onClick={onLogoutClicked}>
                            <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path fillRule="evenodd" clipRule="evenodd" d="M7.70718 5.29291L6.29297 6.70712L11.5859 12L6.29297 17.2929L7.70718 18.7071L14.4143 12L7.70718 5.29291ZM12.7072 5.29291L11.293 6.70712L16.5859 12L11.293 17.2929L12.7072 18.7071L19.4143 12L12.7072 5.29291Z" fill="black"/>
                            </svg>
                            <div className={classes.logoutText}>Logout</div>
                        </div>
                    </div>
                </div>
            </Toolbar>
        </AppBar>
    )
}
