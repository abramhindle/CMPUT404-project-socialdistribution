import * as React from 'react';
import Card from '@mui/material/Card';
import CardHeader from '@mui/material/CardHeader';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import GitHubIcon from '@mui/icons-material/GitHub';
import { capitalize, startCase } from 'lodash/fp';

/* 
 * Takes the date formatted according to the ISO standard and returns the date formatted in the form "March 9, 2016 - 6:07 AM"
 */
function isoToHumanReadableDate(isoDate) {
  const date = new Date(isoDate);
  const dateFormat = new Intl.DateTimeFormat('en', { year: 'numeric', month: 'long', day: 'numeric' });
  const timeFormat = new Intl.DateTimeFormat('en', { hour: 'numeric', minute: 'numeric' });
  return dateFormat.format(date) + " - " + timeFormat.format(date);
}

/*
 * Gets message to display based on github event type
 */
function getGithubMessage(event) {
  var message = ""
  switch (event.type) {
    case "CommitCommentEvent":
      message = "Created a commit comment in " + event.repo.name 
      break;
    case "CreateEvent":
      message = "Created a " + event.payload.ref_type + " in " + event.repo.name
      break;
    case "DeleteEvent":
      message = "Deleted " + event.payload.ref_type + " in " + event.repo.name
      break;
    case "ForkEvent":
      message = "Forked " + event.payload.forkee.full_name + " from " + event.repo.name
      break;
    case "GollumEvent":
      message = "Updated " + event.payload.pages.length + " page(s) in " + event.repo.name +":\n"
      event.payload.pages.forEach((page) => message += "• " + page.title + "\n")
      break;
    case "IssueCommentEvent":
      message = capitalize(event.payload.action) + " issue comment in " + event.repo.name
      break;
    case "IssuesEvent":
      message = capitalize(event.payload.action) + " issue in " + event.repo.name
      break;
    case "PublicEvent":
      message = "Changed " + event.repo.name + " from private to public"
      break;
    case "PullRequestEvent":
      message = capitalize(event.payload.action) + " pull request in " + event.repo.name
      break;
    case "PullRequestReviewEvent":
      message = capitalize(event.payload.action) + " pull request review in " + event.repo.name
      break;
    case "PullRequestReviewCommentEvent":
      message = capitalize(event.payload.action) + " pull request review comment in " + event.repo.name
      break;
    case "PushEvent":
      message = "Pushed " + event.payload.size + " commit(s) to " + event.repo.name + ":\n"
      event.payload.commits.forEach((commit) => message += "• " + commit.message + "\n")
      break;
    case "ReleaseEvent":
      message = capitalize(event.payload.action) + " release in " + event.repo.name
      break;
    case "SponsorshipEvent":
      message = capitalize(event.payload.action) + " sponsorship in " + event.repo.name
      break;
    case "WatchEvent":
      message = capitalize(event.payload.action) + " watching " + event.repo.name
      break;
  }
  return message
}

export default function GithubFeedCard({ event }) {
  /* State Hook For Colour Scheme */
  const [color, setColor] = React.useState("grey");
  
  const handleColor = (event) =>{
    setColor("secondary")
  }

  return (
    <Card sx={{m: "1px"}}>
      <CardHeader
        avatar={ <GitHubIcon sx={{ width: 64, height: 64}} /> }
        title={<Typography variant='h6'>{startCase(event.type)}</Typography>}
        subheader={
          <span>
            <Typography variant='subheader'>{isoToHumanReadableDate( event.created_at )}</Typography>
          </span> }
        disableTypography={true}
      />
      <CardContent>
        <Box sx={{width: "100%", px: "80px", }}>
          <Typography paragraph style={{whiteSpace: 'pre-line'}}>
            { getGithubMessage( event ) }
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
}