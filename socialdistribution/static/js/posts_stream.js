/**
 * Displays the github activities of the user
 * 
 */
var markup = '<div class="post-card">\
<!--start of the post heading-->\
<div class="post-heading">\
    <div class="post-author">\
        <div class="post-author-img">\
            <img src="${event.actor.avatar_url}"  alt="">\
        </div>\
        <div class="post-author-body">\
            <p class="post-author-name">GitHub Activity - ${event.actor.display_login}</p>\
            <p class="post-timestampe">${event.created_at}</p>\
        </div>\
    </div>\
</div>\
<!--end of the post heading-->\
<!--start of the post item-->\
<div class="post-item">\
    <h5 class="post-card-title">${event.type} on</h5>\
    <a class="post-card-text" href="https://github.com/${event.repo.name}">${event.repo.name}</a>\
    {{if event.type == "PullRequestEvent"}}\
    <p>${event.payload.pull_request.body}</p>\
    {{else event.type == "PullRequestReviewCommentEvent" }}\
    <p>${event.payload.comment.body}</p>\
    {{else event.type == "IssueCommentEvent" }}\
    <p><a href="${event.payload.comment.html_url}">detail</a></p>\
    {{else event.type == "IssuesEvent" }}\
    <p><a href="${event.payload.issue.html_url}">${event.payload.issue.title}</a></p>\
    {{/if}}\
</div>\
<!--end of the post item-->'


$(document).ready(function() {
    var authorId = $(".profile-header-info").attr("id");
    var githubName;
    $.template( "githubTemplate", markup );

    /**
     * Get the Github Account of the authenticated user,
     * and then make a Github API event request to get all the events
     * from the Github.
     */
    $.ajax({
        url: '/api/author/' + authorId,
        method: 'GET',
        success: function(result) {
            githubName = result.github.split("/")[3];
            githubName = githubName.toLowerCase();
        },
        error: function(request,msg,error) {
            console.log('fail to get user github');
        }
    }).done(function() {
        $.ajax({
            url: 'https://api.github.com/users/' + githubName + '/events',
            method: 'GET',
            success: function(events) {
                for (event of events) {
                    console.log(event);
                    console.log(event.created_at);
                    // console.log($(template_author).ready());
                    $.tmpl( "githubTemplate", event ).appendTo("#my-stream" );
                }
            },
            error: function(request,msg,error) {
                console.log('fail to get the the github stream');
            }
        });  
    }); 
});