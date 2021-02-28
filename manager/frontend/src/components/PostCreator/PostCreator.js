import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import InputBase from '@material-ui/core/InputBase';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

const useStyles = makeStyles(() => ({
    root: {
        backgroundColor: 'white',
        padding: '1em 1em'
    },
    divider: {
        margin: '1em 1em',
        opacity: '0.2'
    },
    title: {
        fontWeight: 'bold',
        fontSize: '0.8em',
        margin: '0em 1em'
    },
    textField: {
        margin: '0em 1em'
    },
    visibility: {
        height: '2.5em',
        width: '12em',
    },
    sendButton: {
        margin: '0em 1em'
    },
    controls: {
        display: 'flex',
        justifyContent: 'flex-end'
    }
}));

export default function PostCreator() {
    const classes = useStyles();
    const [visibility, setVisibility] = React.useState('default');

    let text = '';

    const visibilityOnClickHandler = (event) => {
        setVisibility(event.target.value);
    }

    const sendButtonHandler = (event) => {
        console.log(text);
    }

    const textFieldChangeHandler = (event) => {
        text = event.target.value;
    }
  
    return (
        <div
            className={classes.root}
        >
            <div className={classes.title}>NEW POST</div>
            <hr className={classes.divider}></hr>
            <InputBase
                className={classes.textField}
                onChange={textFieldChangeHandler}
                multiline
                rows={6}
                placeholder='Write Something ...'
                fullWidth
            />
            <div className={classes.controls}>
                <FormControl variant='outlined' className={classes.formControl}>
                    <Select
                        value={visibility}
                        onChange={visibilityOnClickHandler}
                        className={classes.visibility}
                    >
                        <MenuItem value='default' disabled>
                            <em>Who can see this</em>
                        </MenuItem>
                        <MenuItem value='public'>Public</MenuItem>
                        <MenuItem value='private'>Private</MenuItem>
                        <MenuItem value='friends'>Friends</MenuItem>
                        <MenuItem value='custom'>Custom</MenuItem>
                    </Select>
                </FormControl>
                <div
                    className={classes.sendButton}
                    onClick={sendButtonHandler}
                >
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect width="32" height="32" rx="4" fill="#D1305E"/>
                        <path d="M21.6667 10.3333L14.3333 17.6666" stroke="white" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M21.6667 10.3333L17 23.6666L14.3333 17.6666L8.33333 14.9999L21.6667 10.3333Z" stroke="white" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                </div>
            </div>
        </div>
    )
}
