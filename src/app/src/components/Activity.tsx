import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import processPayload from '../utils/GithubUtils';
import Link from '@mui/material/Link';

interface props {
  type: string;
  payload: any;
  repo: any;
}
const renderTypes = (type: string, newPayload: any) => {
  switch (type) {
    case 'PullRequestReviewEvent':
      return (
        <Card sx={{ minWidth: 100 }}>
          <CardContent>
            {newPayload?.review.state.toUpperCase() + ' '}
            <Link href="newPayload?.url">Pull Request</Link> by {newPayload?.assignee}
          </CardContent>
        </Card>
      );
    default:
      return null;
  }
};
const Activity = ({ type, payload, repo }: props) => {
  const newPayload = processPayload(payload, type);
  return <>{renderTypes(type, newPayload)}</>;
};
export default Activity;
