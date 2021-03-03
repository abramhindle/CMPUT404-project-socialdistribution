import React from 'react';
import { useHistory } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

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
}));

export default function Navbar() {
    const classes = useStyles();
    const history = useHistory();
    
    const onIconClick = (e) => {
        history.push("/profile");
    };

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
                            <div className={classes.logo}></div>
                        </div>
                        <div className={'col-4'}>
                            <div
                                className={classes.icon}
                                onClick={onIconClick}
                            ></div>
                        </div>
                    </div>
                </div>
            </Toolbar>
        </AppBar>
    )
}
