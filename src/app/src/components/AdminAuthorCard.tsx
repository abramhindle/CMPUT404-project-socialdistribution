import * as React from "react"
import { Card, CardContent, Button, ButtonGroup, Box, Typography} from "@mui/material"

export default function AdminAuthorCard({
    author,
}: {
    author: {id:string, displayName:string, profileImage?:string|null}
}): JSX.Element {

    const buttons = [
        <Button onClick={()=>alert("Go to Edit User Page")}key="edit" > Edit </Button>,
        <Button onClick={()=>alert("Delete user")} key="del"> Delete </Button>,
    ];

    return (
        <Card 
            variant="outlined" 
            sx={{
            m:2,
            boxShadow:2,
            }}
        >
            <CardContent sx={{
                width: 700,
                height:80,
            }}>
                <Box display="flex" sx={{
                        width: '100%',
                        height:'100%',
                }}>
                    <Box display="flex" sx={{
                        width: '50%',
                        alignItems: 'center',
                    }}>
                        <Box display="block">
                            <Typography sx={{ fontWeight: 'bold' }}>
                                {author.id}
                            </Typography>

                            <Typography>
                                {author.displayName}
                            </Typography>
                        </Box>

                    </Box>

                    <Box display="flex" flexDirection="row-reverse"sx={{
                        width: '50%',
                        alignItems: 'center',
                    }}>
                        <ButtonGroup variant="contained" size="large">
                            {buttons}
                        </ButtonGroup>

                    </Box>
                </Box>
            </CardContent>
        </Card>
  );
};

