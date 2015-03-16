from datetime import datetime
from django.core.cache import cache
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.utils.html import format_html, format_html_join
from post.models import Post, VisibleToAuthor, PostImage
from author.models import Author
from images.forms import DocumentForm
from comment.models import Comment

import requests
import uuid
import json

import logging

logger = logging.getLogger(__name__)


def createPost(request):
    context = RequestContext(request)

    if request.method == "POST":
        if request.user.is_authenticated():
            title = request.POST.get("title", "")
            description = request.POST.get("description", "")
            content = request.POST.get("text_body", "")
            author = Author.objects.get(user=request.user)
            visibility = request.POST.get("visibility_type", "")
            # TODO: not sure whether to determine type or have user input type
            content_type = "text/plain"

            new_post = Post.objects.create(title=title,
                                           description=description,
                                           guid=uuid.uuid1(),
                                           content=content,
                                           content_type=content_type,
                                           visibility=visibility,
                                           author=author)

            # TODO: should prob not do this
            if visibility == Post.ANOTHER_AUTHOR:
                try:
                    # TODO somehow change this to get the actual author
                    visible_author = request.POST.get("visible_author", "")
                    visible_author_obj = Author.getAuthorWithUserName(visible_author)

                    VisibleToAuthor.objects.create(
                        visibleAuthor=visible_author_obj, post=new_post)
                except Author.DoesNotExist:
                    # TODO: not too sure if care about this enough to handle it
                    print("hmm")

            # TODO: handle multiple image upload
            if len(request.FILES) > 0 and 'thumb' in request.FILES:
                profile = DocumentForm(request.POST, request.FILES)
                image = DocumentForm.createImage(profile, request.FILES['thumb'])
                PostImage.objects.create(post=new_post, image=image)
        else:
            return redirect('login.html', 'Please log in.', context)

    return redirect(index)


# def modifyPost(request):


def deletePost(request, post_id):
    context = RequestContext(request)

    if request.user.is_authenticated():
        Post.deletePost(post_id)
    else:
        return _render_error('login.html', 'Please log in.', context)

    return redirect(index)


def index(request):
    context = RequestContext(request)

    if request.method == 'GET':
        if request.user.is_authenticated():
            try:
                post_instance = Post()
                author = Author.objects.get(user=request.user)
                post_list = (Post.getVisibleToAuthor(author) + _get_github_events(author))
                visibility_types = post_instance.getVisibilityTypes()

                context['posts'] = _getDetailedPosts(post_list)
                context['visibility'] = visibility_types

                return render_to_response('index.html', context)
            except Author.DoesNotExist:
                return _render_error('login.html', 'Please log in.', context)
        else:
            return _render_error('login.html', 'Please log in.', context)

def posts(request, author_id):
    context = RequestContext(request)

    if request.method == 'GET':
        try:
            if request.user.is_authenticated():
                viewer = Author.objects.get(user=request.user)
            else:
                viewer = None
            author = Author.objects.get(uuid=author_id)
            post_list = (Post.getVisibleToAuthor(viewer, author) + _get_github_events(author))

            context['posts'] = _getDetailedPosts(post_list)
            context['specific'] = True #context indicating that we are seeing a specific user stream

            return render_to_response('index.html', context)
        except Exception as e:
            print "Error in posts: %s" % e

# def post(request, post_id):
# return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def _getDetailedPosts(post_list):
    images = []
    comments = []

    for post in post_list:
        images.append(PostImage.objects.filter(post=post).select_related('image'))
        comments.append(Comment.objects.filter(post=post))

    parsed_posts = list(zip(post_list, images, comments))

    # Sort posts by date
    parsed_posts.sort(key=lambda
        item: item[0].publication_date,
                    reverse=True)

    return parsed_posts


def _get_github_events(author):
    """Retrieves all the public events for the given GitHub author.

    Events are retrieved from GitHub's API at
    https://api.github.com/users/<user>/events

    GitHub has a rate limit of 60. In order to not exhaust the limit as
    quickly, the events are cached. A GitHub E-tag is also stored, and used
    in the header of the request so that GitHub will not count the request
    towards the rate limit if events are unchanged.
    """
    headers = {'Connection': 'close'}

    if len(author.github_etag) > 0:
        headers['If-None-Match'] = author.github_etag

    url = 'https://api.github.com/users/%s/events' % author.github_user

    response = requests.get(url, headers=headers)

    # print response

    # We didn't get a response or we've reached our GitHub limit of 60.
    if not response or int(response.headers["X-RateLimit-Remaining"]) == 0:
        return []

    if response.status_code == 200:
        # Store the etag for future use
        author.github_etag = response.headers['ETag']
        author.save()

        events = []

        for event in response.json():
            content = _build_github_event_text(event, author)
            if content is not None:
                # Construct the GitHub event post
                post = Post(content=content,
                            content_type=Post.PLAIN_TEXT,
                            visibility=Post.PRIVATE,
                            author=author,
                            publication_date=datetime.strptime(
                                event['created_at'], '%Y-%m-%dT%H:%M:%SZ'))
                events.append(post)

        # Cache these results in the event that we've reached our rate
        # limit, or we get a 304 because the events haven't changed.
        cache.set(author.user.id, events, None)
        return events
    elif response.status_code == 304:
        # Results haven't changed, let's just return the cache, if one exists,
        # otherwise, we need to get it again.
        cached = cache.get(author.user.id)
        if cached is None:
            author.github_etag = ''
            return _get_github_events(author)
        else:
            return cached
    else:
        # print 'ERROR: API at %s returned %d' % url, response.status_code
        return []


def _build_github_event_text(event, author):
    """Generate HTML based on a GitHub event type.

    The event types are found here:
    https://developer.github.com/v3/activity/events/types/

    Only the most frequent events will be addressed here. I.e. deprecated
    events such as DownloadedEvent and FollowEvent will not be supported.
    """
    event_type = event['type']
    payload = event['payload']

    if event_type == 'CommitCommentEvent':
        # Commented on a commit.
        url = payload['comment']['html_url']
        commit = payload['comment']['commit_id']
        content = payload['comment']['body'][0:400] + '...'
        repo = event['repo']['name']

        return format_html("<p><strong>{0}</strong> commented on commit "
                           "<a href='{1}'>{2}@{3}</a></p><p>{4}</p>",
                           author.github_user, url, repo, commit, content)

    elif event_type == 'CreateEvent':
        # Created a repository, branch, or tag.
        url = event['repo']['url']
        ref_type = payload['ref_type']
        ref = payload['ref']

        return format_html("<p><strong>{0}</strong> created a "
                           "<a href='{1}'>{2}</a>: {3}</p>",
                           author.github_user, url, ref_type, ref)

    elif event_type == 'DeleteEvent':
        # Deleted a branch or tag.
        url = payload['repository']['html_url']
        ref_type = payload['ref_type']
        ref = payload['ref']

        return format_html("<p><strong>{0}</strong> deleted a "
                           "<a href='{1}'>{2}</a>: {3}</p>",
                           author.github_user, url, ref_type, ref)

    elif event_type == 'ForkEvent':
        # Triggered when a user forks a repository.
        forkee = payload['forkee']['full_name']
        forkee_url = payload['forkee']['html_url']
        repo = event['repo']['name']
        url = 'http://www.github.com/%s' % repo
        name = event['repo']['name']

        return format_html("<p><strong>{0}</strong> forked "
                           "<a href='{1}'>{2}</a> to "
                           "<a href='{3}'>{4}</a></p>",
                           author.github_user, url, name, forkee_url, forkee)

    elif event_type == 'GollumEvent':
        # Triggered when a Wiki page is created or updated.
        pages = payload['pages']

        content = ''
        for page in pages:
            content += "<p><strong>%s</strong> %s the " \
                       "<a href='%s'>%s</a> wiki.</p>" % \
                       (author.github_user, page['action'],
                        page['html_url'], page['title'])

        return format_html(content)

    elif event_type == 'IssueCommentEvent':
        # Triggered when an issue comment is created.
        issue_url = payload['issue']['html_url']
        issue_num = payload['issue']['number']
        comment = payload['comment']['body']

        return format_html("<p><strong>{0}</strong> commented on Issue "
                           "<a href='{1}'>{2}</a></p><p>{3}</p>",
                           author.github_user, issue_url, issue_num, comment)

    elif event_type == 'IssuesEvent':
        # Triggered when an issue comment is created.
        issue_url = payload['issue']['html_url']
        issue_num = payload['issue']['number']
        action = payload['action']

        return format_html("<p><strong>{0}</strong> {1} Issue "
                           "<a href='{2}'>{3}</a></p>",
                           author.github_user, action, issue_url, issue_num)

    elif event_type == 'MemberEvent':
        # Triggered when a user is added as a collaborator.
        member = payload['member']['login']
        member_url = payload['member']['html_url']
        repo = event['repo']['name']

        return format_html("<p><a href='{0}'><strong>{1}</strong></a> was "
                           "added as a collaborator to {2}.</p>",
                           member_url, member, repo)

    elif event_type == 'PublicEvent':
        # Triggered when a private repository is open sourced :)
        repo = event['repo']['name']
        url = 'http://www.github.com/%s' % repo

        return format_html("<p><a href='{0}'>{1}</a> was made public.</p>",
                           url, repo)

    elif event_type == 'PullRequestEvent':
        # Triggered on a pull request
        pull = payload['number']
        pull_url = payload['pull_request']['html_url']
        action = payload['action']
        title = payload['pull_request']['title']

        return format_html("<p>Pull Request <a href='{0}'>{1}</a> "
                           "was {2}.</p><p>{3}</p>",
                           pull_url, pull, action, title)

    elif event_type == 'PullRequestReviewCommentEvent':
        # Triggered when a comment is created on a pull request
        pull = payload['number']
        pull_url = payload['pull_request']['html_url']
        title = payload['pull_request']['title']
        comment = payload['comment']['body']
        comment_url = payload['comment']['html_url']

        return format_html("<p>A <a href='{0}'>comment</a> was made on Pull "
                           "Request <a href='{1}'>{2}</a><i>{3}</i>.</p><p>"
                           "{4}</p>",
                           comment_url, pull_url, pull, title, comment)

    elif event_type == 'PushEvent':
        # Triggered when a repository branch is pushed to.
        commits = payload['commits']
        repo = event['repo']['name']
        url = 'http://www.github.com/%s' % repo
        content = "<p><strong>%s</strong> pushed to <a href='%s'>%s</a></p>" \
                  % (author.github_user, url, repo)

        for commit in commits:
            content += "<p>%s</p>" % commit['message']

        return format_html(content)

    elif event_type == 'WatchEvent':
        # Related to starring a repository, not watching
        repo = event['repo']['name']
        url = 'http://www.github.com/%s' % repo

        return format_html("<p><strong>{0}</strong></a>  "
                           "starred <a href='{1}'>{2}</a>.</p>",
                           author.github_user, url, repo)

    else:
        return None



def _render_error(url, error, context):
    context['error'] = error
    return render_to_response(url, context)
