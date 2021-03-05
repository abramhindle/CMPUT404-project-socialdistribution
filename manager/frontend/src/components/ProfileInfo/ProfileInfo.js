import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

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
    }
  }));

export default function ProfileInfo(props) {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <div className={classes.name}>
                { props.profile.displayName }            
            </div>
            <div className={classes.container}>
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
            </div>
            <div>
                { props.profile.github }
            </div>
        </div>
    )
}
