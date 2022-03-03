import * as React from "react"
import { Box, List, ButtonGroup, Button , Badge, Typography, Divider} from "@mui/material"
import NavBar from "../components/NavBar"
import ManageRequestsRequests from "../components/ManageRequestsRequests"
import ManageRequestsFriends from "../components/ManageRequestsFriends"
import ManageRequestsFollowing from "../components/ManageRequestsFollowing"
import ManageRequestsFollowers from "../components/ManageRequestsFollowers"

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

    const friends = [
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

    const following = [
        {
        id:"07a931d8-b181-473d-8fdssd8-22dfb5c81416",
        displayName:"Tony Stark",
        profileImage:null,
        },
        {
        id:"c3293ed4-e55e-4986-8311-5ad43a27f5a3",
        displayName:"The Rock",
        profileImage:"",
        },
    ];

    const followers = [
        {
        id:"07a931d8-b181-473d-8fdssd8-22dfb5c81416",
        displayName:"Chris Hemsworth",
        profileImage:null,
        },
        {
        id:"c3293ed4-e55e-4986-8311-5ad43a27f5a3",
        displayName:"Kevin Hart",
        profileImage:"",
        },
    ];

    // Get length for badges
    const totalRequests = followRequests.length;
    const totalFriends = friends.length;
    const totalFollowing = following.length;
    const totalFollowers = followers.length;

    const buttons: Array<string>=["Requests", "Friends", "Following", "Followers"]

    const handleonClick = (whichone: string) => {
      switch (whichone) {
        case "Requests":
            setListDisplay({title:'Follow Requests',id:0})
            break;
        case "Friends":
            setListDisplay({title:'Friends',id:1})
            break;
        case "Following":
            setListDisplay({title:'Following',id:2})
            break;
        case "Followers":
            setListDisplay({title:'Followers',id:3})
            break;
      }
    };

    const returnLength = (whichone: string) => {
        switch (whichone) {
          case "Requests":
              return totalRequests;
          case "Friends":
              return totalFriends;
          case "Following":
              return totalFollowing;
          case "Followers":
              return totalFollowers;
        }
      };

    const returnKey = (whichone: string) => {
        switch (whichone) {
          case "Requests":
              return "requests"
          case "Friends":
              return "friends"
          case "Following":
              return "following"
          case "Followers":
              return "followers";
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
        followRequests.map((user) => (
            <ManageRequestsRequests user={user} key={user.id}/>
        )),
        friends.map((friend) => (
            <ManageRequestsFriends user={friend} key={friend.id}/>
        )),
        following.map((user) => (
            <ManageRequestsFollowing user={user} key={user.id}/>
        )),
        followers.map((user) => (
            <ManageRequestsFollowers user={user} key={user.id}/>
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