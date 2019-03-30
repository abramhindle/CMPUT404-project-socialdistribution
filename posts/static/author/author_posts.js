function follow_user(other, user) {
    let authheader = Cookies.get('authheader');
    let body = {
        query: 'friendrequest',
        author: {
            'id': document.getElementById("request_maker_id").value,
            'host': document.getElementById("request_maker_host").value,
            'displayName': document.getElementById("request_maker_display_name").value,
            'url': document.getElementById("request_maker_url").value,
        },
        friend: {
            'id': document.getElementById("request_receiver_id").value,
            'host': document.getElementById("request_receiver_host").value,
            'displayName': document.getElementById("request_receiver_display_name").value,
            'url': document.getElementById("request_receiver_url").value,
        },
    };
    fetch('/friendrequest', {
        method: 'post',
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Basic ${authheader}`,
        },
        body: JSON.stringify(body)
    }).then((res) => {
        window.location.reload(true)
    });
}

function unfollow_user(id) {
    let authheader = Cookies.get('authheader');
    fetch(`/follow/${id}/`, {
        method: 'delete',
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Basic ${authheader}`,
        },
    }).then((res) => {
        window.location.reload(true)
    });
}

async function pull_github_activity() {
    let github = document.getElementsByName("github")[0].value;
    let oldId = document.getElementsByName('githubLastId')[0].value;
    //let fetches = [];
    let authheader = Cookies.get('authheader');

    let githubsplit = github.split("/");
    let githubUsername = githubsplit[githubsplit.length - 1];

    let response = await fetch("https://api.github.com/users/" + githubUsername + "/events", {
        method: 'get'
    });
    let activity = await response.json();

    for (var i = 0; i < 10; i++) {
        if (activity[i]['id'] == oldId) {
            break;
        }

        var body = create_github_post(activity[i]);

        await fetch('/posts/', {
            method: 'post',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Basic ${authheader}`,
            },
            body: JSON.stringify(body)
        })
    }

    let newId = activity[0]['id'];
    let gitbody = {"id" : newId}

    await fetch('/frontend/author/github/', {
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Basic ${authheader}`,
        },
        body: JSON.stringify(gitbody)
    });

    window.location.reload(true);
}


function create_github_post(response) {

    if (response["type"] == "PushEvent") {
        var event_type = " pushed to ";
    } else if (response["type"] == "IssuesEvent") {
        var event_type = " made an issue on ";
    } else if (response["type"] == "ForkEvent") {
        var event_type = " forked ";
    } else if (response["type"] == "IssueCommentEvent") {
        var event_type = " commented on an issue on ";
    } else if (response["type"] == "CreateEvent") {
        var event_type = " created the repository ";
    } else {
        var event_type = " did something on ";
    }

    let post =
        {
            title: "Github Activity",
            description: "Github Activity",
            content: response["actor"]["display_login"] + event_type + response["repo"]["name"],
        }

    return post;
}