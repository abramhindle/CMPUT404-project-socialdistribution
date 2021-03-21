import React, { useState } from 'react';
import { connect } from 'react-redux';

import { emphasize, makeStyles } from '@material-ui/core/styles';
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
    button: {
        margin: '0em 0.5em',
        marginTop: '0.2em',
        '&:hover': {
            backgroundColor: '#FFCCCB',
            fill: 'white'
        },
        height: 'fit-content'
    },
    controls: {
        display: 'flex',
        justifyContent: 'flex-end'
    },
    testTitle: {
        margin: '0em 1em',
        fontWeight: 'bold',
    },
    textTags: {
        padding: '0em 1em',
        margin: '0.5em 0em'
    }
}));

export default function PostCreator(props) {
    const classes = useStyles();

    const [visibility, setVisibility] = useState('default');
    const [type, setType] = useState('default');
    const [title, setTitle] = useState('');
    const [text, setText] = useState('');
    const [tags, setTags] = useState([]);

    const dropdownOnClickHandler = (event) => {
        switch (event.target.name) {
            case 'visibility':
                setVisibility(event.target.value);
                break;
            case 'content-type':
                setType(event.target.value);
                break;
            default:
                break;
        }
    }

    const addImageButton = (e) => {
        console.log('add image button clicked');
    }

    const sendButtonHandler = (e) => {
        props.createNewPost({
            content: text,
            title,
            visibility,
            contentType: type,
            categories: tags
        })
    }

    const onTextChange = (e) => {
        switch (e.target.id) {
            case 'textTitle':
                setTitle(e.target.value);
                break;
            case 'textBody':
                setText(e.target.value);
                break;
            case 'textTags':
                setTags(e.target.value.split(','));
            default:
                break;
        }
    }
  
    return (
        <div
            className={classes.root}
        >
            <div className={classes.title}>NEW POST</div>
            <hr className={classes.divider}></hr>
            <InputBase
                className={classes.testTitle}
                onChange={onTextChange}
                placeholder='Title'
                fullWidth
                id='textTitle'
            />
            <InputBase
                className={classes.textField}
                id='textBody'
                onChange={onTextChange}
                multiline
                rows={6}
                placeholder='Write Something ...'
                fullWidth
            />
            <InputBase
                className={classes.textField, classes.textTags}
                onChange={onTextChange}
                placeholder='Tags (separate with commas)'
                fullWidth
                id='textTags'
            />
            <div className={classes.controls}>
                <FormControl variant='outlined' className={classes.formControl}>
                    <Select
                        value={type}
                        onChange={dropdownOnClickHandler}
                        className={classes.visibility}
                        name='content-type'
                    >
                        <MenuItem value='default' disabled>
                            <em>Content Type</em>
                        </MenuItem>
                        <MenuItem value='text/markdown'>Markdown</MenuItem>
                        <MenuItem value='text/plain'>Plain Text</MenuItem>
                        <MenuItem value='image/png;base64'>Image PNG</MenuItem>
                        <MenuItem value='image/jpeg;base64'>Image JPEG</MenuItem>
                    </Select>
                </FormControl>
                <FormControl variant='outlined' className={classes.formControl}>
                    <Select
                        value={visibility}
                        onChange={dropdownOnClickHandler}
                        className={classes.visibility}
                        name='visibility'
                    >
                        <MenuItem value='default' disabled>
                            <em>Who can see this</em>
                        </MenuItem>
                        <MenuItem value='PUBLIC'>Public</MenuItem>
                        <MenuItem value='PRIVATE'>Private</MenuItem>
                        <MenuItem value='FRIENDS'>Friends</MenuItem>
                        <MenuItem value='CUSTOM'>Custom</MenuItem>
                    </Select>
                </FormControl>
                <div
                    className={classes.button}
                    onClick={addImageButton}
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g opacity="0.15">
                        <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M8.5 10C9.32843 10 10 9.32843 10 8.5C10 7.67157 9.32843 7 8.5 7C7.67157 7 7 7.67157 7 8.5C7 9.32843 7.67157 10 8.5 10Z" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        <path d="M21 15L16 10L5 21" stroke="black" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </g>
                    </svg>
                </div>
                <div
                    className={classes.button}
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
