import React from 'react';
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        margin: '10px 10px',
        display: 'flex',
        '&:hover': {
            backgroundColor: '#FFCCCB',
        },
    },
    addButton: {
        borderRadius: '30px',
        padding: '0px 0px',
        minWidth: '2em',
        marginLeft: 'auto'
    }
  }));  

export default function Person(props) {
    const classes = useStyles();

    const clickHandler = () => {
        props.personClicked(props.person);
    }

    return (
        <div className={classes.root} onClick={clickHandler}>
            {props.person.displayName}
        </div>
    )
}
