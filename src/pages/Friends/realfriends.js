import "../pages.css";
import "./friends.css";

import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { get_friends_for_author } from "../../api/follower_api";
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

import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Sidebar from "../../components/Sidebar/sidebar";

function Realfriends() {
  const user = useSelector((state) => state.user);
  const author_id = `http://localhost/authors/${user.id}/`;
  const [follow_list, setList] = useState({ items: [] });
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const location = useLocation();

  useEffect(() => {
    get_friends_for_author(user.id, setList);
  }, []);

  const Details = (follow_id) => {
    //TODO redirect to the realfriends page
  };

  const onSuccess = () => {
    setSuccess(true);
  };

  const goBack = () => {
    navigate("/");
  };

  

  return ( 
    <>
      <Sidebar/>
      <div className="sidebar-offset">
        <div>
        <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar variant="dense" className="table-head">
          <Typography variant="h6" align="left" color="inherit" component="div">
            Realfriends
          </Typography>
          <Button
                variant="contained"
                id="back"
                onClick={goBack}
                >
                back
            </Button>
          </Toolbar>
        </AppBar>
        </Box>
        </div>
        <TableContainer component={Paper} className="table-container">
        <Table sx={{ minWidth: 650 }} aria-label="simple table" className="table">
          <TableHead className="table-titles">
            <TableRow>
              <TableCell id="title">ID</TableCell>
              <TableCell id="title" align="right">Name</TableCell>
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
              </TableRow>
            ))}
          </TableBody>
        </Table>  
        </TableContainer>
  
      </div>
    </>
  );
}
  

export default Realfriends;
