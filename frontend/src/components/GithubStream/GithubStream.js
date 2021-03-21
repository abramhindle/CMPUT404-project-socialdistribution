import React, { useState } from 'react';

import Activity from './Activity/Activity';

import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
    root: {
        // height: '300px',
        backgroundColor: 'white',
        marginBottom: '40px',
        borderRadius: "8px",
    },
    github: {
        padding: '1em 1em',
        display: 'flex'
    },
    title: {
        marginLeft: '1em'
    },
    arrow: {
        marginLeft: 'auto'
    }
}));

export default function GithubStream(props) {
    const classes = useStyles();

    const [activities, setActivities] = useState(null);
    const [expanded, setExpanded] = useState(false);

    const headerClicked = () => {
        if (!expanded) {
            if (props.activities.length > 0) {
                setActivities(props.activities.map((d, i) => <Activity key={i} activity={d}/>));
            }
            setExpanded(true);
        } else {
            setActivities(null);
            setExpanded(false);
        }
    }

    const arrow = expanded 
        ? <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fillRule="evenodd" clipRule="evenodd" d="M12.0001 9.41421L4.70718 16.7071L3.29297 15.2929L12.0001 6.58578L20.7072 15.2929L19.293 16.7071L12.0001 9.41421Z" fill="black"/>
        </svg>
        : <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fillRule="evenodd" clipRule="evenodd" d="M19.293 7.29291L20.7072 8.70712L12.0001 17.4142L3.29297 8.70712L4.70718 7.29291L12.0001 14.5858L19.293 7.29291Z" fill="black"/>
        </svg>;


    return (
        <div className={classes.root}>
            <div
                className={classes.github}
                onClick={headerClicked}
            >
                <div>
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
                    <span className={classes.title}>Github Activity</span>
                </div>
                <div className={classes.arrow}>
                    {arrow}
                </div>
            </div>
            { activities }
        </div>
    )
}
