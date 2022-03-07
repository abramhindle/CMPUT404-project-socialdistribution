import * as React from "react"
import { Card, CardContent, Button, Box, Typography} from "@mui/material"

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
                        <Box display="block">
                            <Typography sx={{ fontWeight: 'bold' }}>
                                {node.id}
                            </Typography>

                            <Typography>
                            {node.username}
                            </Typography>
                        </Box>

                    </Box>

                    <Box display="flex" flexDirection="row-reverse"sx={{
                        width: '50%',
                        alignItems: 'center',
                    }}>
                        <Button variant="contained" size="large" onClick={()=>alert('Deleted node')}>
                            Delete
                        </Button>

                    </Box>
                </Box>
            </CardContent>
        </Card>
  );
};

