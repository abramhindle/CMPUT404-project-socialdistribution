import * as React from "react"
import { Card, CardContent, Button, ButtonGroup, Typography, Box} from "@mui/material"

export default function AdminRequestCard({
    request,
}: {
    request: {id:string, displayName:string}
}): JSX.Element {

    const buttons = [
        <Button onClick={()=>alert("Accepted user!")}key="accept" > Accept </Button>,
        <Button onClick={()=>alert("Rejected User")} key="reject"> Reject </Button>,
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
                width: '90%',
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
                        <Typography sx={{ fontWeight: 'bold' }}>
                            {request.displayName}
                        </Typography>
                        <Typography style={{ marginLeft: 5 }}>
                            wants to signup.
                        </Typography>
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
