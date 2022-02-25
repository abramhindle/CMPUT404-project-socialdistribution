let newPayload: any = {};
const processPayload = (payload: any, type: string) => {
  if (type === 'PullRequestReviewEvent') {
    newPayload['url'] = payload?.pull_request?.url;
    newPayload['review'] = {
      url: payload?.review?.html_url,
      reviewMessage: payload?.review?.body,
      state: payload?.review?.state,
    };
    newPayload['assignee'] = payload?.pull_request?.user?.login;
  }

  return newPayload;
};

export default processPayload;
