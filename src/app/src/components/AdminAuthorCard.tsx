import * as React from "react"
import { Card, CardContent} from "@mui/material"

export default function AdminAuthorCard(): JSX.Element {
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
                Authors
            </CardContent>
        </Card>
  );
};

