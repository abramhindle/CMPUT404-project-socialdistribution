let newPayload: any = {};

const getHTMLURLfromSha = (commits: any, size: number) => {
  let arr: Array<string> = [];
  for (let i = 0; i < size; i++) {
    let url = commits[i]['url'];
    url = url?.replace('api.', '');
    url = url?.replace('commits', 'commit');
    url = url?.replace('/repos', '');
    arr.push(url);
  }
  return arr;
};
const processPayload = (payload: any, type: string) => {
  switch (type) {
    case 'PullRequestReviewEvent':
      newPayload['url'] = payload?.pull_request?.html_url;
      newPayload['review'] = {
        url: payload?.review?.html_url,
        reviewMessage: payload?.review?.body,
        state: payload?.review?.state,
      };
      newPayload['assignee'] = payload?.pull_request?.user?.login;
      break;
    case 'PushEvent':
      newPayload['url'] = getHTMLURLfromSha(payload?.commits, payload?.size);
      newPayload['branch'] = payload?.ref.split('/')[payload?.ref.split('/').length - 1];
  }
  return newPayload;
};

export default processPayload;
