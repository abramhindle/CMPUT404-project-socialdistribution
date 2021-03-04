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
        backgroundColor: 'lightgray',
        padding: '0em 1em',
        margin: '0.5em 0em'
    }
}));

export default function PostCreator(props) {
    const classes = useStyles();

    const [visibility, setVisibility] = React.useState('default');
    const [type, setType] = React.useState('default');
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

    const addGithubButton = (e) => {
        console.log('github clicked');
    }

    const sendButtonHandler = (e) => {
        props.createNewPost({
            text,
            title,
            visibility,
            type,
            tags
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
                        <MenuItem value='public'>Public</MenuItem>
                        <MenuItem value='private'>Private</MenuItem>
                        <MenuItem value='friends'>Friends</MenuItem>
                        <MenuItem value='custom'>Custom</MenuItem>
                    </Select>
                </FormControl>
                
                <div
                    className={classes.button}
                    onClick={addGithubButton}
                >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g clipPath="url(#clip0)">
                        <path d="M16 21.9999V18.1299C16.0375 17.6531 15.9731 17.1737 15.811 16.7237C15.6489 16.2737 15.3929 15.8634 15.06 15.5199C18.2 
                            15.1699 21.5 13.9799 21.5 8.51994C21.4997 7.12376 20.9627 5.78114 20 4.76994C20.4559 3.54844 20.4236 2.19829 19.91 
                            0.999938C19.91 0.999938 18.73 0.649938 16 2.47994C13.708 1.85876 11.292 1.85876 9 2.47994C6.27 0.649938 5.09 
                            0.999938 5.09 0.999938C4.57638 2.19829 4.54414 3.54844 5 4.76994C4.03013 5.78864 3.49252 7.1434 3.5 8.54994C3.5 13.9699 
                            6.8 15.1599 9.94 15.5499C9.611 15.8899 9.35726 16.2953 9.19531 16.7399C9.03335 17.1844 8.96681 17.658 9 18.1299V21.9999M9 
                            18.9999C4 20.4999 4 16.4999 2 15.9999L9 18.9999Z" stroke="#E0E0E0" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                        </g>
                        <defs>
                        <clipPath id="clip0">
                        <rect width="24" height="24" fill="white"/>
                        </clipPath>
                        </defs>
                    </svg>
                </div>
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
