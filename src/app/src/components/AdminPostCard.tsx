import * as React from "react"
import { Card, CardContent, Box, Typography } from "@mui/material"
import Post from "../api/models/Post";

export default function AdminPostCard({
    post,
}: {
    post: Post
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
                <Box display="block" sx={{
                        width: '100%',
                        height:'100%',
                }}>
                    
                    <Typography sx={{ fontWeight: 'bold' }}>
                            {post.id}
                    </Typography>

                    <Typography>
                        {post.origin}
                    </Typography>

                    <Typography>
                        {post.published}
                    </Typography>

                </Box>
            </CardContent>
        </Card>
  );
};

