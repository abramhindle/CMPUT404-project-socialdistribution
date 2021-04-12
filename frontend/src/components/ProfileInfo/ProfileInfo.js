import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

import { useHistory } from "react-router-dom";

const useStyles = makeStyles(() => ({ 
    root: {
		marginBottom: "30px",
        height: '200px',
        backgroundColor: 'white',
        padding: '1em',
		borderRadius: '10px',
		boxShadow: '2px 2px 4px'
    },
    name: {
        fontWeight: 'bold',
        fontSize: '1.5em',
        marginBottom: '1em',
    },
    container: {
        display: 'flex',
        justifyContent: 'space-between'
    },
    linkButton: {
        margin: '0.5em 0',
        fontSize: '1em',
        borderRadius: "20px",
        textAlign: "center",
        padding: "0.25em",
        border: "1px solid #D3D3D3",
        cursor: "pointer",
        '&:hover': {
            backgroundColor: '#D3D3D3',
        }
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
                className={classes.linkButton}
                onClick={ handleGoManageProfile }
            >
                Manage Profile            
            </div>
            
            <div style={{ textAlign: "center" }}>
                { props.profile.github }
            </div>
        </div>
    )
}
