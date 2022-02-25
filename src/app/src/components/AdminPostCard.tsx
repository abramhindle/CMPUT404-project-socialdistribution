import * as React from "react"
import { Card, CardContent } from "@mui/material"

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
                justifyContent: 'center',
            }}>
                {post.id} {post.author.displayName} {post.date}
            </CardContent>
        </Card>
  );
};

