function follow_user(other, user) {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let body = {
        author: user,
        friend: other,
        csrfmiddlewaretoken: csrf
    };
    fetch('/friendrequest/', {
        method: 'post',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        body: JSON.stringify(body)
    }).then((res) => {
        window.location.reload(true)
    });
}

function unfollow_user(id) {
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let body = {
        csrfmiddlewaretoken: csrf
    };
    fetch(`/follow/${id}/`, {
        method: 'delete',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        },
        body: JSON.stringify(body)
    }).then((res) => {
        window.location.reload(true)
    });
}

// taken from https://stackoverflow.com/questions/951021/what-is-the-javascript-version-of-sleep
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function pull_github_activity(){
    let github = document.getElementsByName("github")[0].value;
    let oldId = document.getElementsByName('githubLastId')[0].value;
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    let fetches = [];

    githubsplit = github.split("/");
    githubUsername = githubsplit[githubsplit.length - 1];

    let response = await fetch("https://api.github.com/users/" + githubUsername + "/events", {
        method: 'get'
    });
    let activity = await response.json();

    for (var i = 0; i < 10; i++) {
        if(activity[i]['id'] == oldId){
            break;
        }

        console.log("adding post");
        await sleep(100);

        var body = create_github_post(activity[i]);
        
        fetches.push(
        // TODO implement basic auth on posting
            fetch('/posts/', {
                method: 'post',
                headers: {
                    "X-CSRFToken": csrf,
                    'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
            })
        );
    }

    await Promise.all(fetches);
    console.log("done post");

    let newId = activity[0]['id'];
    let formData = new FormData();
    formData.append("newId", newId);
    formData.append("csrfmiddlewaretoken", csrf);

    await fetch('/frontend/author/github/', {
        method: 'post',
        headers: {
            "X-CSRFToken": csrf
        },
        body: formData
    });

    window.location.reload(true);
}


function create_github_post(response){
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if(response["type"] == "PushEvent"){
        var event_type = " pushed to ";
    }else if(response["type"] == "IssuesEvent"){
        var event_type = " made an issue on ";
    }else if(response["type"] == "ForkEvent"){
        var event_type = " forked ";
    }else if(response["type"] == "IssueCommentEvent"){
        var  event_type = " commented on an issue on ";
    }else if(response["type"] == "CreateEvent"){
        var event_type = " created the repository ";
    }else{
        var event_type = " did something on ";
    }

    post = 
        {
            title : "Github Activity",
            description : "Github Activity",
            content : response["actor"]["display_login"] + event_type + response["repo"]["name"],
            csrfmiddlewaretoken: csrf
    }

    return post;
}