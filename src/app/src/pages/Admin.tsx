import * as React from "react"
import { Box, List, ButtonGroup, Button , Badge, Typography, Divider} from "@mui/material"
import NavBar from "../components/NavBar"
import AdminRequestCard from "../components/AdminRequestCard"
import AdminAuthorCard from "../components/AdminAuthorCard"
import AdminPostCard from "../components/AdminPostCard"
import AdminNodeCard from "../components/AdminNodeCard"

export default function Admin(): JSX.Element {
    const [listDisplay, setListDisplay] = React.useState({title:'Requests',id:0});

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

    const authors = [
        {
        id:"07a931d8-b181-473d-8838-22dfb5c81416",
        displayName:"Lara Croft",
        profileImage:null,
        },
        {
        id:"c3293ed4-e55e-4986-8311-5ad43a27f5a3",
        displayName:"Nathan Drake",
        profileImage:null,
        },
    ];

    const posts=[
        {
        id:"07a931d8-b181-473d-8838-22dfb5c81416",
        author:authors[0],
        date: "2022-02-25"
        }
    ];

    const nodes=[
        {
        id:"07a931d8-b181-473d-8838-22dfb5c81416",
        username:"NodeOne",
        }
    ];

    // Get length for badges
    const totalRequests = signupRequests.length;
    const totalAuthors = authors.length;
    const totalPosts = posts.length;
    const totalNodes = nodes.length;

    const buttons: Array<string>=["Requests", "Authors", "Posts", "Nodes"]

    const handleonClick = (whichone: string) => {
      switch (whichone) {
        case "Requests":
            setListDisplay({title:'Requests',id:0})
            break;
        case "Authors":
            setListDisplay({title:'Authors',id:1})
            break;
        case "Posts":
            setListDisplay({title:'Posts',id:2})
            break;
        case "Nodes":
            setListDisplay({title:'Nodes',id:3})
            break;
      }
    };

    const returnLength = (whichone: string) => {
        switch (whichone) {
          case "Requests":
              return totalRequests;
          case "Authors":
              return totalAuthors;
          case "Posts":
              return totalPosts;
          case "Nodes":
              return totalNodes;
        }
      };

    const returnKey = (whichone: string) => {
        switch (whichone) {
          case "Requests":
              return "requests"
          case "Authors":
              return "authors"
          case "Posts":
              return "posts"
          case "Nodes":
              return "nodes";
        }
      };

    let buttonSx = {
        justifyContent:"space-between",
        display: "flex",
    };

    let badgeSx = {
        justifyContent:"right", 
        mx:3
    };

    // Lists to display per button
    const lists=[
        signupRequests.map((request) => (
            <AdminRequestCard request={request} key={request.id}/>
        )),
        authors.map((author) => (
            <AdminAuthorCard author={author} key={author.id}/>
        )),
        posts.map((post) => (
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
                    {buttons.map((item:string) => <Button onClick={() => handleonClick(item)} key={returnKey(item)} sx={buttonSx}>{item}<Badge badgeContent={returnLength(item)} color="secondary" sx={badgeSx}/></Button>)}
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