import * as React from "react";
import { Box, List, ButtonGroup, Button , Badge, Typography, Divider} from "@mui/material";
import NavBar from "../components/NavBar";
import AdminRequestCard from "../components/AdminRequestCard";
import AdminAuthorCard from "../components/AdminAuthorCard";
import AdminPostCard from "../components/AdminPostCard";
import AdminNodeCard from "../components/AdminNodeCard";
import Author from "../api/models/Author";
import Post from "../api/models/Post";
import api from "../api/api";
import { useState, useEffect } from 'react';

export default function Admin(): JSX.Element {
    //Some fake data to help with layouts
    const signupRequests = [
        {
        id:"07a931d8-b181-473d-8838-22dfb5c81416",
        displayName:"Lara Croft",
        },
        {
        id:"c3293ed4-e55e-4986-8311-5ad43a27f5a3",
        displayName:"Nathan Drake",
        },
    ];

    //Get author from backend
    const [authors, setAuthors] = useState<Author[] | undefined>(undefined)
    
    useEffect(() => {
        api.authors
        .list()
        .then((data)=>setAuthors(data))
        .catch((error) => {console.log('No authors')})
    }, [])

    //Need to be able to get all posts
    const [posts, setPosts] = useState<Post[] | undefined>(undefined)
    //Temporary posts for now
    const id = "dd1258c7-2853-4f17-bd96-6ff10c2ffb24";
    useEffect(() => {
        api.authors
        .withId(id)
        .posts
        .list(1,5)
        .then((data)=>setPosts(data))
        .catch((error) => {console.log(error)})
    }, [id,posts])

    const nodes=[
        {
        id:"07a931d8-b181-473d-8838-22dfb5c81416",
        username:"NodeOne",
        }
    ];

    // Get length for badges
    const totalRequests = signupRequests.length;
    const totalAuthors = (authors)?authors.length:0;
    const totalPosts = (posts)?posts.length:0;
    const totalNodes = nodes.length;

    //Set which to display
    const [listDisplay, setListDisplay] = React.useState({id:0,title:'Requests', count:totalRequests});

    const buttonStyle = {
        justifyContent:"space-between", 
        display: "flex"
    }

    const badgeStyle = {
        justifyContent:"right", 
        mx:3
    }

    // Sidebar Button group
    const buttons = [
        {id:0,title:'Requests', count:totalRequests},
        {id:1,title:'Authors',count:totalAuthors},
        {id:2,title:'Posts',count:totalPosts},
        {id:3,title:'Nodes',count:totalNodes}
    ];

    // Lists to display per button
    const lists=[
        signupRequests.map((request) => (
            <AdminRequestCard request={request} key={request.id}/>
        )),
        authors?.map((author) => (
            <AdminAuthorCard author={author} key={author.id}/>
        )),
        posts?.map((post) => (
            <AdminPostCard post={post} key={post.id}/>
        )),
        nodes.map((node) => (
            <AdminNodeCard node={node} key={node.id}/>
        ))
    ];
      
    return (
    <>
    <Box sx={{ height: window.innerHeight,width: window.innerWidth}}>
        <Box style={{ height: '5%' }} sx={{ bgcolor:"#fff"}}>
            <NavBar items={[
            {
                Text: "",
                handleClick: () => {
                console.log(1);
                },
            },
            ]} />
        </Box>
        <Box style={{ display: 'flex', height: "95%" }} sx={{ bgcolor:"#fff"}}>
            <Box display="flex" sx={{
                    flexDirection: 'column',
                    width: '30%',
                    alignItems: 'center',
                    bgcolor:"#fff",
                    ml:2,
                    mt:9,
                }}>

                <ButtonGroup
                    orientation="vertical"
                    aria-label="vertical contained button group"
                    variant="contained"
                    size="large"
                    fullWidth={true}
                >
                    {buttons.map((button) => (
                        <Button onClick={()=>setListDisplay(button)}key={button.id} sx={buttonStyle}> {button.title} <Badge badgeContent={button.count} color="secondary" sx={badgeStyle}/></Button>
                    ))}

                </ButtonGroup>
                
                {listDisplay.title ==='Authors'?(
                    <Button onClick={()=>alert("Add Author Page")} variant='contained' fullWidth={true} sx={{mt:5}}>Add</Button>
                ):null}

                {listDisplay.title==='Nodes'?(
                     <Button onClick={()=>alert("Add Node Page")} variant='contained' fullWidth={true} sx={{mt:5}}>Add</Button>
                ):null}
    
            </Box>

            <Box overflow="auto" display="flex" sx={{
                flexDirection: 'column',
                width: '70%',
                alignItems: 'center',
                mt:0.5
            }}>
                <Typography variant="h4">{listDisplay.title}</Typography>
                <Divider style={{width:'85%'}}></Divider>
                <List style={{maxHeight: '100%', overflow: 'auto'}}>
                    {lists[listDisplay.id]}
                </List>,
            </Box>
        </Box>
    </Box>
    </>
)
}