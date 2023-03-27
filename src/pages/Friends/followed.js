import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { get_followed_for_author } from "../../api/follower_api";
import { delete_followers_for_author } from "../../api/follower_api";
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

function Followed() {
  const user = useSelector((state) => state.user);
  const author_id = `http://localhost/authors/${user.id}/`;
  const [follow_list, setList] = useState({ items: [] });
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const location = useLocation();

  useEffect(() => {
    get_followed_for_author(user.id, setList);
  }, []);

  const DeleteAuthor = (follow_id) => {
    delete_followers_for_author(user.id, follow_id, onSuccess);
  };

  const onSuccess = () => {
    setSuccess(true);
  };

  const goBack = () => {
    navigate("/");
  };

  return (
    <>
      <Sidebar />
      <div className="sidebar-offset">
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar variant="dense">
              <Button variant="contained" onClick={goBack}>
                back
              </Button>
              <Typography
                variant="h6"
                align="left"
                color="inherit"
                component="div"
              >
                Followed
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
                    color="error"
                    onClick={(e) => DeleteAuthor(row.id)}
                  >
                    Delete
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
}

export default Followed;
