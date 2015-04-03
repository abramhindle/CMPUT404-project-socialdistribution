from django.core.cache import cache
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect, QueryDict, HttpResponse
from django.template import RequestContext
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from post.models import Post, VisibleToAuthor, PostImage
from author.models import Author
from images.forms import DocumentForm
from category.models import PostCategory, Category
import node.APICalls as remote_helper

import dateutil.parser
import post.utils as post_utils

import requests
import uuid
import json

import logging

logger = logging.getLogger(__name__)

# def modifyPost(request):

# default page is time line


def index(request):
    context = RequestContext(request)
    if request.method == 'GET':
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponseRedirect('/api/author/posts', status=302)
        else:
            if request.user.is_authenticated():
                try:
                    # get only posts made by friends and followees
                    viewer = Author.objects.get(user=request.user)
                    return render_to_response('index.html', _getAllPosts(viewer=viewer, friendsOnly=True), context)
                except Author.DoesNotExist:
                    return _render_error('login.html', 'Please log in.', context)
            else:
                return _render_error('login.html', 'Please log in.', context)

    elif request.method == 'DELETE':
        try:
            if request.user.is_authenticated():
                post_utils.deletePost(QueryDict(request.body).get('post_id'))

                return HttpResponse(json.dumps({'msg': 'post deleted'}),
                                    content_type="application/json")
            else:
                return _render_error('login.html', 'Please log in.', context)
        except Exception as e:
            print "Error in posts: %s" % e

    elif request.method == 'POST':
        try:
            if request.user.is_authenticated():
                title = request.POST.get("title", "")
                description = request.POST.get("description", "")
                content = request.POST.get("text_body", "")
                author = Author.objects.get(user=request.user)
                visibility = request.POST.get("visibility_type", "")
                content_type = Post.MARK_DOWN if request.POST.get(
                    "markdown_checkbox", False) else Post.PLAIN_TEXT
                categories = request.POST.get("categories", "")

                new_post = Post.objects.create(title=title,
                                               description=description,
                                               guid=uuid.uuid1(),
                                               content=content,
                                               content_type=content_type,
                                               visibility=visibility,
                                               author=author)

                if visibility == Post.ANOTHER_AUTHOR:
                    try:
                        visible_author = request.POST.get("visible_author", "")
                        visible_author_obj = Author.get_author_with_username(
                            visible_author)

                        VisibleToAuthor.objects.create(
                            visibleAuthor=visible_author_obj, post=new_post)
                    except Author.DoesNotExist:
                        # TODO: not too sure if care about this enough to
                        # handle it
                        print("hmm")

                # TODO: handle multiple image upload
                if len(request.FILES) > 0 and 'thumb' in request.FILES:
                    profile = DocumentForm(request.POST, request.FILES)
                    image = DocumentForm.createImage(
                        profile, request.FILES['thumb'])
                    PostImage.objects.create(post=new_post, image=image)

                category_list = categories.split(',')
                for category in category_list:
                    PostCategory.addCategoryToPost(new_post, category)

                viewer = Author.objects.get(user=request.user)
                return render_to_response('index.html', _getAllPosts(viewer=viewer, friendsOnly=True), context)
            else:
                return redirect('login.html', 'Please log in.', context)
        except Exception as e:
            print "Error in posts: %s" % e

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Get all the posts that are visible to the current viewer
# Note: if no one is logged in, then all posts that have public visibility
# is shown
def public(request):
    context = RequestContext(request)
    if request.method == 'GET':
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponseRedirect('/api/posts', status=302)
        else:
            if request.user.is_authenticated():
                viewer = Author.objects.get(user=request.user)
            else:
                viewer = None

            data = _getAllPosts(viewer=viewer)
            data['specific'] = True
            data['page_header'] = 'All posts visible to you'
            data['category_list'] = mark_safe(Category.getListOfCategory())

            return render_to_response('index.html', data, context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def posts(request, author_id):
    context = RequestContext(request)

    if request.method == 'GET':
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponseRedirect('/api/author/%s/posts' % author_id, status=302)
        else:
            try:
                if request.user.is_authenticated():
                    viewer = Author.objects.get(user=request.user)
                else:
                    viewer = None

                author = Author.objects.get(uuid=author_id)
                data = _getAllPosts(viewer=viewer, postAuthor=author)
                data['page_header'] = 'Posts by %s' % author.user.username

            except Exception as e:
                data = _getAllPosts(
                    viewer=viewer, postAuthor=author_id, remoteOnly=True)

            data['specific'] = True  # context indicating that we are seeing a specific user stream
            data['category_list'] = mark_safe(Category.getListOfCategory())

            return render_to_response('index.html', data, context)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def post(request, post_id):
    context = RequestContext(request)

    if request.method == 'GET' or request.method == 'POST':
        if 'application/json' in request.META['HTTP_ACCEPT']:
            return HttpResponseRedirect('/api/posts/%s' % post_id, status=302)
        else:
            try:
                if request.user.is_authenticated():
                    viewer = Author.objects.get(user=request.user)
                else:
                    viewer = None
                post = post_utils.getPostById(post_id, viewer)

                # if request.type == 'application/json':
                # return
                # HttpResponse(json.dumps(post_utils.get_post_json(post)))
                context['posts'] = _getDetailedPosts([post])
                # context indicating that we are seeing a specific user stream
                context['specific'] = True
                context['page_header'] = 'Posts with ID %s' % post_id
                context['category_list'] = mark_safe(Category.getListOfCategory())

                return render_to_response('index.html', context)
            except Exception as e:
                print "Error in posts: %s" % e

    elif request.method == 'PUT':
        if request.user.is_authenticated():
            try:
                jsonData = json.load(request.body)
                viewer = Author.objects.get(user=request.user)
                post = post_utils.getPostById(post_id, viewer)
                title = jsonData['title']
                description = jsonData['description']
                content = jsonData['content']
                content_type = jsonData['content-type']
                visibility = jsonData['visibility']
                if post is None:
                    if title is not None:
                        post.title = title
                    if description is not None:
                        post.description = description
                    if content is not None:
                        post.content = content
                    if content_type is not None:
                        post.content_type = content_type
                    if visibility is not None:
                        post.visibility = visibility
                else:
                    if viewer == post.author:
                        if (title is None or
                                visibility is None or
                                description is None or
                                content is None or
                                content_type is None):
                            return HttpResponse('missing required fields',
                                                content_type='text/plain',
                                                status=500)
                        post = Post(guid=post_id, title=title, description=description, content=content,
                                    content_type=content_type,
                                    visibility=visibility, author=viewer)
                    else:
                        # user editing is not the author of the post
                        return HttpResponse(status=403)
                post.save()
                return HttpResponse(json.dumps(post_utils.get_post_json(post)), content_type='application/json')
            except Author.DoesNotExist:
                return HttpResponse(status=403)
        else:
            return HttpResponse(status=403)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def taggedPosts(request, tag):
    context = RequestContext(request)

    if request.method == 'GET':
        try:
            if request.user.is_authenticated():
                postList = []
                viewer = Author.objects.get(user=request.user)
                posts = post_utils.getVisibleToAuthor(viewer)
                taggedPosts = PostCategory.getPostWithCategory(tag)

                for categorizedPost in taggedPosts:
                    jsonPost = post_utils.get_post_json(categorizedPost.post)
                    if jsonPost in posts:
                        postList.append(jsonPost)

                context['posts'] = _getDetailedPosts(postList)
                context['visibility'] = post_utils.getVisibilityTypes()
                context['category_list'] = mark_safe(Category.getListOfCategory())
                context['page_header'] = 'Posts tagged as %s' % tag
                context['specific'] = True

                return render_to_response('index.html', context)
        except Exception as e:
            print "Error in posts: %s" % e

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# TODO this is a bad design but if remoteonly is called postAuthor pass in
# is a string other wise its an object :/


def _getAllPosts(viewer, postAuthor=None, friendsOnly=False, remoteOnly=False):
    data = {}

    if remoteOnly:
        post_list = remote_helper.api_getPostByAuthorID(viewer, postAuthor)
    else:
        post_list = post_utils.getVisibleToAuthor(viewer=viewer,
                                                  author=postAuthor,
                                                  time_line=friendsOnly)
        if viewer is not None:
            post_list.extend(_get_github_events(viewer))

    data['posts'] = _getDetailedPosts(post_list)
    data['visibility'] = post_utils.getVisibilityTypes()
    data['category_list'] = mark_safe(Category.getListOfCategory())

    return data


def _getDetailedPosts(post_list):
    images = []
    hacked_posts = []

    for post in post_list:
        images.append(PostImage.objects.filter(post__guid=post['guid']).select_related('image'))


        if 'pubdate' in post:
            post['pubDate'] = post['pubdate']
        hacked_posts.append(post)

    parsed_posts = list(zip(hacked_posts, images))

    # Sort posts by date
    parsed_posts.sort(key=lambda
                      item: dateutil.parser.parse(item[0]['pubDate']),
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
                            publication_date=dateutil.parser.parse(event['created_at']))
                events.append(post.getJsonObj())

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
        url = event['repo']['url']
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
