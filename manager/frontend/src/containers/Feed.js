import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import _ from 'lodash';

import Navbar from '../components/Navbar/Navbar';
import PostCreator from '../components/PostCreator/PostCreator';
import PostSorter from '../components/PostSorter/PostSorter';
import Posts from '../components/Posts/Posts';
import Friends from '../components/Friends/Friends';

const useStyles = makeStyles(() => ({
    posts: {
    },
    feed: {
    },
    container: {
        padding: '0px 10%'
    }
  }));


export default function Feed() {
    const classes = useStyles();
    const postClasses = [classes.posts, 'col-9', 'pe-5']
    const container = ['container-fluid', classes.container];

    const temp_posts = [
        {title: 'post1'},
        {title: 'post2'},
        {title: 'post3'},
        {title: 'post4'},
    ];

    const temp_friends = [
        {name: 'Friend1'},
        {name: 'Friend2'},
        {name: 'Friend3'},
        {name: 'Friend4'},
        {name: 'Friend5'},
    ];


    return (
        <div 
            className={classes.feed}
        >
            <Navbar />
            <div className={container.join(' ')}>
                <div className='row align-items-start'>
                    <div className={postClasses.join(' ')}>
                        <PostCreator />
                        <PostSorter />
                        <Posts posts={temp_posts} />
                    </div>
                    <div className='col-3 ps-5'>
                        <Friends friends={temp_friends}/>
                    </div>
                </div>
            </div>            
        </div>
        
    )
}