import * as React from "react"
import { Card, CardContent, Button, ButtonGroup} from "@mui/material"

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
                width: 700,
                height:80,
                justifyContent: 'center',
            }}>
                {request.displayName} wants to signup.
                <ButtonGroup variant="contained" size="large">
                    {buttons}
                </ButtonGroup>
            </CardContent>
        </Card>
  );
};

