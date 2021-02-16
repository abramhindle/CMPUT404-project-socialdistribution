import React from 'react'
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(() => ({
  root: {
    flexGrow: 1,
    backgroundColor: "#FFF",
    marginBottom: "30px"
  },
}));

export default function Navbar() {
    const classes = useStyles();

    return (
        <AppBar
            className={classes.root}
            position="static"
            elevation={0}
        >
            <Toolbar >
                <Typography variant="h6" color="textPrimary">
                    Konnect
                </Typography>
            </Toolbar>
        </AppBar>
    )
}
