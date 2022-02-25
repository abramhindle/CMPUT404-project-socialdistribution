import * as React from "react"
import { Card, CardContent, Button} from "@mui/material"

export default function AdminNodeCard({
    node,
}: {
    node: {id:string, username:string}
}): JSX.Element {

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
                {node.id} {node.username}
                <Button variant="contained" size="large" onClick={()=>alert("Delete node")}>
                    Delete
                </Button>
            </CardContent>
        </Card>
  );
};

