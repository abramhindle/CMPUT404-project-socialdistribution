//import './friends.css';
import { get_author }from '../../api/author_api'
import { get_all_authors }from '../../api/author_api'
import { useEffect, useState } from "react";
import { useSelector } from "react-redux"
import { add_followers_for_author } from '../../api/follower_api';
import { add_request } from '../../api/follower_api';
import { post_inbox } from "../../api/inbox_api";
import { useLocation, useNavigate } from "react-router-dom";

import * as React from "react";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Button from "@mui/material/Button";

import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';



function Friends() {

    const user = useSelector((state) => state.user);
    const author_id = `http://localhost/authors/${user.id}/`
    const [follow_list, setList] = useState({"items": []}); 
    const [success, setSuccess] = useState(null); 
    const navigate = useNavigate();
    
    let page = 1;

    const location = useLocation();

    useEffect(() => { 
      get_all_authors(page, setList)
      
    }, []);

    const get_search_params = () => {
      const queryParams = new URLSearchParams(location.search);
      const query_page = queryParams.get("page");
  
      if (query_page) page = parseInt(query_page);
    };
    
    get_search_params();

    //no need to handle anything here
    const followAuthor= (object) => {
        const actor = user;
        
        const obj = {
          "type":"follow",
          "Summary":user.displayName + "wants to follow" + object.displayName,
          "actor":actor,
          "object":object
        }

        post_inbox(user.id,obj,onSuccess)
        //add_request(user.id, obj, onSuccess)
        //add_followers_for_author(user.id, follow_id, onSuccess)
    }

    const onSuccess = () => {
        setSuccess(true);
    }
    
    const page_buttons = () => {
 
        if (follow_list.items.length < 5 && page == 1)
        {
          return;
        }
        if (page == 1)
        {
            return (<button onClick={forward_page}>Next Page</button>);
        } 
        else if (follow_list.items.length < 5)
        {
          return <button onClick={back_page}>Prev Page</button>
        } 
        else 
        {
          return (
          <div>
            <button onClick={back_page}>Prev Page</button>
            <button onClick={forward_page}>Next Page</button>
          </div>);
        }
      };


    const forward_page = () => {
        page = page + 1;
        navigate(`/friends/?page=${page}`);
        navigate(0)
      };
    
    const back_page = () => {
        page = page - 1;
        navigate(`/friends/?page=${page}`);
        navigate(0)
      };
    
    const goBack = () => {
        navigate("/");
      };
  
  
    return (
        
        <>
        <div>
        <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar variant="dense">
            <Button
                variant="contained"
                onClick={goBack}
                >
                back
            </Button>
          <Typography variant="h6" align="left" color="inherit" component="div">
            Add friends
          </Typography>
          </Toolbar>
        </AppBar>
        </Box>
        </div>
        <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell align="right">Name</TableCell>
              <TableCell align="right">Follow</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {follow_list.items.map((row) => (
              <TableRow
                key={row.id}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.id}
                </TableCell>
                <TableCell align="right">{row.displayName}</TableCell>
                <TableCell align="right">
                  <Button
                    variant="contained"
                    onClick={(e) => followAuthor(row)}
                  >
                    follow
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>  
      </TableContainer>
      <div style={{ width: "100%", textAlign: "center", paddingTop: 16 }}>
          {page_buttons()}
      </div>
      

      </>
    );
  }
  



export default Friends;