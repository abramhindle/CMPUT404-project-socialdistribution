import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import { useHistory } from "react-router-dom";

const useStyles = makeStyles(() => ({
    root: {
        height: '200px',
        backgroundColor: 'white',
        padding: '1em 1em',
        backgroundColor: 'red',
        background: 'linear-gradient(#FFC0CB 3.5em, white 90%)'
    },
    name: {
        fontWeight: 'bold',
        fontSize: '1.5em',
        marginBottom: '1em'
    },
    container: {
        display: 'flex',
        justifyContent: 'space-between'
    },
    link: {
        marginTop: '1em'
    }
  }));

export default function ProfileInfo(props) {
    const classes = useStyles();

    const history = useHistory();

    // click on the Comments count to see the full post, with its paginated comments
    const handleGoManageProfile = () => {
        history.push("/manage-profile")
    }

    return (
        <div className={classes.root}>
            <div className={classes.name}>
                { props.profile.displayName }            
            </div>
            <div 
                className={classes.name}
                onClick={ handleGoManageProfile }
            >
                Manage Profile            
            </div>
            {/* <div className={classes.container}>
                <div>
                    Friends
                    <br/>
                    { props.numFriends }
                </div>
                <div >
                    Followers
                    <br/>
                    { props.numFollowers }
                </div>
            </div> */}
            <div className={classes.link}>
                { props.profile.github }
            </div>
        </div>
    )
}
