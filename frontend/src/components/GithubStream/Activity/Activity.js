import React from 'react';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
    },
    info: {
        color: '#H3H3H3',
        fontSize: '0.75em',
        padding: '0em 2em',
        paddingTop: '1em'
    },
    divider: {
        margin: '0em 1em',
        opacity: '0.2'
    }
}));

export default function Activity(props) {
    const classes = useStyles();

    return (
        <div>
            <p className={classes.info}>
                {props.activity.actor.display_login} made {props.activity.type} on {props.activity.created_at.split('T')[0]}
            </p>
            <hr className={classes.divider}></hr>
        </div>
    )
}
