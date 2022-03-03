import * as React from "react"
import { Card, CardContent, Box, Typography } from "@mui/material"

export default function AdminPostCard({
    post,
}: {
    post: {id:string, author:{id:string, displayName:string, profileImage?:string|null}, date:string}
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
            }}>
                <Box display="block" sx={{
                        width: '100%',
                        height:'100%',
                }}>
                    
                    <Typography sx={{ fontWeight: 'bold' }}>
                            {post.id}
                    </Typography>

                    <Typography>
                        {post.author.displayName}
                    </Typography>

                    <Typography>
                        {post.date}
                    </Typography>

                </Box>
            </CardContent>
        </Card>
  );
};

