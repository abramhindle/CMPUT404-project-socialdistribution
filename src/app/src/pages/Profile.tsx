import * as React from "react"
import { Box, Card, IconButton, Avatar, List, CardContent, Button, Typography } from "@mui/material"
import GitHubIcon from "@mui/icons-material/GitHub"
import PersonIcon from "@mui/icons-material/Person"
import NavBar from "../components/NavBar";

export default function Profile(): JSX.Element {
    const author = {
        displayName: 'John Doe',
        github: 'github',
        profileImage: null,
        friends:2,
        followers:10,
        following:5
    }

    // If it's your profle - Edit
    // If you follow them - Unfollow
    // You sent them a request - Request Sent
    // Else - Follow
    const myProfile = false;
    const [isFollowing, setFollowing] = React.useState(true);
    const [sentRequest, setRequestSent] = React.useState(false);

    const handleFollow = () => {
        setRequestSent(true);
    }

    const handleUnfollow = () => {
        setFollowing(false);                     
    }

    if (author !== undefined){
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
                <Box boxShadow={5} display="flex" sx={{
                        flexDirection: 'column',
                        width: '30%',
                        justifyContent: 'center',
                        alignItems: 'center',
                        bgcolor:"#fff",
                    }}>

                        {author.profileImage?(
                            null
                        ):
                        <Avatar sx={{ width: 150, height: 150, m:2}}>
                            <PersonIcon
                                sx={{ width: 100, height: 100 }}
                            />
                        </Avatar>}
                        
                        <Typography variant="h4" align="center">
                            {author.displayName}
                        </Typography>
                        {author.github?(
                            <IconButton
                                onClick={() =>
                                    window.open(
                                        `https://www.github.com/${author.github}`
                                    )
                                }
                            ><GitHubIcon/>
                            </IconButton>):null}
        
                            <Box sx={{
                                    marginBottom:2,
                                }}>
                                <Typography variant="h6" align="center">
                                Friends: {author.friends}
                                </Typography>
                                <Typography variant="h6" align="center">
                                    Followers: {author.followers}
                                </Typography>
                                <Typography variant="h6" align="center">
                                    Following: {author.following}
                                </Typography>
                            </Box>
                            
                        {myProfile?(
                        <Button
                            variant="contained"
                            onClick={() => {
                                alert('Clicked Edit Button');
                            }}
                            >
                            Edit
                        </Button>
                        ):
                        isFollowing?(
                            <Button 
                            variant="contained"
                            onClick={handleUnfollow}
                            >
                            Unfollow
                            </Button>
                        ):
                        sentRequest?(
                            <Button 
                            variant="contained"
                            disabled
                            >
                            Request Sent
                            </Button>
                        ):
                        <Button 
                        variant="contained"
                        onClick={handleFollow}
                        >
                        Follow
                        </Button>
                        }
        
                </Box>

                <Box overflow="auto" display="flex" sx={{
                    flexDirection: 'column',
                    width: '70%',
                    alignItems: 'center',
                    mt:0.5
                }}>
                    <List style={{maxHeight: '100%', overflow: 'auto'}}>
                        {[1, 2, 3,4,5,6,7,8,9,10].map((i) => (
                            <Card 
                                key={i} 
                                variant="outlined" 
                                sx={{
                                m:2
                                }}
                            >
                                <CardContent sx={{
                                    width: 700,
                                    height:80,
                                    justifyContent: 'center',
                                }}>
                                    Hi
                                </CardContent>
                            </Card>
                        ))} 
                    </List>
                </Box>
            </Box>
        </Box>
        </>
    )
    }
    return <Box/>
}