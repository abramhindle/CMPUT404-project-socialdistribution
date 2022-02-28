import * as React from "react"
import { Box, List, ButtonGroup, Button , Badge, Typography, Divider} from "@mui/material"
import NavBar from "../components/NavBar"
import AdminAuthorCard from "../components/AdminAuthorCard"
import AdminPostCard from "../components/AdminPostCard"
import AdminNodeCard from "../components/AdminNodeCard"
import ManageFollowRequests from "../components/ManageRequestsRequests"

export default function ManageRequests(): JSX.Element {
    const [listDisplay, setListDisplay] = React.useState({title:'Follow Requests',id:0});

    //Some fake data to help with layouts
    const followRequests = [
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
        profileImage:"",
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
    const totalRequests = followRequests.length;
    const totalAuthors = authors.length;
    const totalPosts = posts.length;
    const totalNodes = nodes.length;

    // Sidebar Button group
    const buttons = [
        <Button onClick={()=>setListDisplay({title:'Follow Requests',id:0})}key="requests" sx={{justifyContent:"space-between", display: "flex"}}> Requests <Badge badgeContent={totalRequests} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
        <Button onClick={()=>setListDisplay({title:'Friends',id:1})} key="friends" sx={{justifyContent:"space-between", display: "flex"}}> Friends <Badge badgeContent={totalAuthors} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
        <Button onClick={()=>setListDisplay({title:'Following',id:2})}key="following" sx={{justifyContent:"space-between", display: "flex"}}> Following <Badge badgeContent={totalPosts} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
        <Button onClick={()=>setListDisplay({title:'Followers',id:3})}key="followers" sx={{justifyContent:"space-between", display: "flex"}}> Followers <Badge badgeContent={totalNodes} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
    ];

    // Lists to display per button
    const lists=[
        followRequests.map((request) => (
            <ManageFollowRequests request={request} key={request.id}/>
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
                    {buttons}
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
                </List>
            </Box>
        </Box>
    </Box>
    </>
)
}