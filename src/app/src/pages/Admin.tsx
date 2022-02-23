import * as React from "react"
import { Box, List, ButtonGroup, Button , Badge, Typography, Divider} from "@mui/material"
import NavBar from "../components/NavBar"
import AdminRequestCard from "../components/AdminRequestCard"
import AdminAuthorCard from "../components/AdminAuthorCard"
import AdminPostCard from "../components/AdminPostCard"
import AdminNodeCard from "../components/AdminNodeCard"

export default function Admin(): JSX.Element {
    const [listDisplay, setListDisplay] = React.useState({title:'Requests',id:0});

    const totalRequests = 200;
    const totalAuthors = 5;
    const totalPosts = 10;
    const totalNodes = 1;

    const buttons = [
        <Button onClick={()=>setListDisplay({title:'Requests',id:0})}key="requests" sx={{justifyContent:"space-between", display: "flex"}}> Requests <Badge badgeContent={totalRequests} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
        <Button onClick={()=>setListDisplay({title:'Authors',id:1})} key="authors" sx={{justifyContent:"space-between", display: "flex"}}> Authors <Badge badgeContent={totalAuthors} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
        <Button onClick={()=>setListDisplay({title:'Posts',id:2})}key="posts" sx={{justifyContent:"space-between", display: "flex"}}> Posts <Badge badgeContent={totalPosts} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
        <Button onClick={()=>setListDisplay({title:'Nodes',id:3})}key="nodes" sx={{justifyContent:"space-between", display: "flex"}}> Nodes <Badge badgeContent={totalNodes} color="secondary" sx={{justifyContent:"right", mx:3}}/></Button>,
    ];

    const lists=[
    <List style={{maxHeight: '100%', overflow: 'auto'}}>
        {[1, 2, 3,4,5,6,7,8,9,10].map((i) => (
            <AdminRequestCard key={i}/>
        ))} 
    </List>,
        <List style={{maxHeight: '100%', overflow: 'auto'}}>
        {[1, 2, 3,4,5,6,7,8,9,10].map((i) => (
            <AdminAuthorCard key={i}/>
        ))} 
    </List>,
        <List style={{maxHeight: '100%', overflow: 'auto'}}>
        {[1, 2, 3,4,5,6,7,8,9,10].map((i) => (
            <AdminPostCard key={i}/>
        ))} 
    </List>,
        <List style={{maxHeight: '100%', overflow: 'auto'}}>
        {[1, 2, 3,4,5,6,7,8,9,10].map((i) => (
            <AdminNodeCard key={i}/>
        ))} 
    </List>
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
    
            </Box>

            <Box overflow="auto" display="flex" sx={{
                flexDirection: 'column',
                width: '70%',
                alignItems: 'center',
                mt:0.5
            }}>
                <Typography variant="h4">{listDisplay.title}</Typography>
                <Divider style={{width:'85%'}}></Divider>
                {lists[listDisplay.id]}
            </Box>
        </Box>
    </Box>
    </>
)
}