import React from "react";
import { Alert, AlertTitle, Container } from "@mui/material";

export type ErrorType = "NotFound" | "Unknown";

const errors: Record<ErrorType, { title: string; description: string }> = {
  NotFound: {
    title: "Page Not Found",
    description: "The page you are looking for does not exist.",
  },
  Unknown: {
    title: "Unknown Error",
    description: "An unknown error occurred.",
  },
};

interface Props {
  errorType: ErrorType;
}

export default function Error({ errorType }: Props) {
  return (
    <Container maxWidth="md">
      <Alert severity="error">
        <AlertTitle>{errors[errorType].title}</AlertTitle>
        {errors[errorType].description}
      </Alert>
    </Container>
  );
}
