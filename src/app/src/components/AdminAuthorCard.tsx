import * as React from "react"
import { Card, CardContent, Button, ButtonGroup} from "@mui/material"

export default function AdminAuthorCard({
    author,
}: {
    author: {id:string, displayName:string, profileImage?:string|null}
}): JSX.Element {

    const buttons = [
        <Button onClick={()=>alert("Edit user")}key="edit" > Edit </Button>,
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
                justifyContent: 'center',
            }}>
                {author.id} {author.displayName}
                <ButtonGroup variant="contained" size="large">
                    {buttons}
                </ButtonGroup>
            </CardContent>
        </Card>
  );
};

