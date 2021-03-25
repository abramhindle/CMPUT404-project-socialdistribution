import React from 'react';
import Button from '@material-ui/core/Button';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        margin: '10px 10px',
        display: 'flex'
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

    const button = props.isSearch ? <Button className={classes.addButton} onClick={props.addClicked} variant="outlined">+</Button> : null

    return (
        <div className={classes.root}>
            {props.friend.displayName}
            { button }
        </div>
    )
}
