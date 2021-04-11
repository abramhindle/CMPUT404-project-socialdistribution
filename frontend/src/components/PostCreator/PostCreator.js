import React, { useState } from 'react';
import { connect } from 'react-redux';
import _ from 'lodash';

import Person from './Person/Person';

import { emphasize, makeStyles } from '@material-ui/core/styles';
import InputBase from '@material-ui/core/InputBase';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import IconButton from '@material-ui/core/IconButton';
import PhotoCamera from '@material-ui/icons/PhotoCamera';

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
    },
    input: {
        display: 'none',
    },
    privatePerson: {
        width: '15em',
        overflow: 'hidden'
    },
    searchWrapper: {
        position: 'relative'
    },
    searchPeopleResult: {
        position: 'absolute',
        backgroundColor: 'white',
        zIndex: '100'
    }
}));

export default function PostCreator(props) {
    const classes = useStyles();

    const [visibility, setVisibility] = useState('default');
    const [type, setType] = useState('default');
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [tags, setTags] = useState([]);
    const [people, setPeople] = useState(props.allAuthors.map((d, i) => <Person key={i} person={d} addClicked={addPersonClicked}/>));
    const [privatePerson, setPrivatePerson] = useState('');

    let searchText = '';

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

    const sendButtonHandler = (e) => {
        if (visibility === 'PRIVATE') {
            props.createNewPost({
                content,
                title,
                visibility,
                contentType: type,
                categories: tags,
            }, privatePerson);
            return;
        }
        props.createNewPost({
            content,
            title,
            visibility,
            contentType: type,
            categories: tags
        });
    }

    const addPersonClicked = (person) => {
        setPrivatePerson(person);
        setPeople(null);
    }

    const onTextChange = (e) => {
        switch (e.target.id) {
            case 'textTitle':
                setTitle(e.target.value);
                break;
            case 'textBody':
                setContent(e.target.value);
                setType('text/plain');
                break;
            case 'textTags':
                setTags(e.target.value.split(','));
                break;
            case 'textURL':
                setContent(e.target.value);
                break;
            case 'textSearch':
                searchText = e.target.value;
                const data = _.filter(props.allAuthors, d => d.displayName.includes(searchText));
                setPeople(data.map((d, i) => 
                    <Person
                        key={i}
                        person={d}
                        personClicked={addPersonClicked}
                    />
                ));
                break;
            default:
                break;
        }
    }

    const onImageUpload = (event) => {
        if (event.target.files.length !== 0) {
            var file = event.target.files[0];
            const reader = new FileReader();
            var url = reader.readAsDataURL(file);
            
            reader.onloadend = function(e) {
                setContent(reader.result);
                setType(event.target.files[0].type);
            }.bind(this);
        }
    }

    const contentBlock = () => {
        let block = null;

        if (type === 'default' || type === 'text/plain' || type === 'text/markdown') {
            block = <InputBase
                className={classes.textField}
                id='textBody'
                onChange={onTextChange}
                multiline
                rows={6}
                placeholder='Write Something ...'
                fullWidth
            />;
        } else if (type ==='image/png' || type === 'image/jpeg') {
            let image_block = null;

            if (content.startsWith('data:image/') || (content.match(/\.(jpeg|jpg|png)$/) != null)) {
                image_block = <img src={content} alt='postimage'/>;
            }

            block = <div>
                <InputBase
                    className={classes.textField, classes.textTags}
                    onChange={onTextChange}
                    placeholder='URL'
                    fullWidth
                    id='textURL'
                />
                { image_block }
            </div>;
        }
        
        return block;
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
            { contentBlock() }
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
                        <MenuItem value='image/png'>Image PNG</MenuItem>
                        <MenuItem value='image/jpeg'>Image JPEG</MenuItem>
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
                { visibility === 'PRIVATE' ? 
                    <div className={classes.searchWrapper}>
                        <InputBase
                            className={classes.textField}
                            onChange={onTextChange}
                            placeholder='Search for someone'
                            id='textSearch'
                        />
                        <div className={classes.searchPeopleResult}>{ people }</div>
                    </div>
                    : null }
                { visibility === 'PRIVATE' ? 
                    <span className={classes.privatePerson}>{ privatePerson.displayName }</span>
                    : null
                }
                <input className={classes.input} id="icon-button-file" type="file" onChange={onImageUpload}/>
                <label htmlFor="icon-button-file">
                    <IconButton color="primary" aria-label="upload picture" component="span">
                        <PhotoCamera />
                    </IconButton>
                </label>
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
