import * as React from 'react';
import { ListItemButton, Avatar, ListItemText, ListItemAvatar, Collapse, Divider, List, ListItemIcon, Typography } from '@mui/material';
import ProfileListItem from './profileListItem';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import { useSelector, useDispatch } from 'react-redux';
import { fontWeight, width } from '@mui/system';

export default function ProfileList({type, profiles, title, author, removeProfile, alertError, alertSuccess}) {
    const profileImage = useSelector(state => state.profile.profileImage);

    const defaultShowCount = 5;
    const [showingCount, setShowingCount] = React.useState(defaultShowCount)

    const handleCollapse = () => { setShowingCount( showingCount === defaultShowCount ? profiles.length : defaultShowCount); }

    const style = {
        title: {
            pl: 2,
            justifyContent: 'center',
            alignItems: 'center', 
            fontWeight: 900
        },
        count: {
            display: 'inline',
            ml: 1,
        },
        listHeader: {
            // background: '#f5f5f5'
        },
        expendIcon: {
            width: 40
        }
    };

    return (
        <List>
            <ListItemText sx={style.title}>{title}:
                <Typography sx={style.count}>{profiles.length}</Typography>
            </ListItemText>
            {profiles.slice(0, showingCount).map((profile, index) => (
                <ProfileListItem key={index} type={type} author={author} profile={profile} removeProfile={removeProfile} alertError={alertError} alertSuccess={alertSuccess} />))}

            {profiles.length > defaultShowCount &&
            <ListItemButton onClick={handleCollapse} sx={style.listHeader}>
                <ListItemText primary={'Show ' + ( Math.abs( profiles.length - defaultShowCount) ) + ' ' + (showingCount === defaultShowCount ? 'More' : 'Less')} />
            </ListItemButton> }
        </List>
    );
} 