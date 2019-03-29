function delete_follow_request(target_user) {
    let authheader = Cookies.get('authheader');
    fetch(`/friendrequest/${target_user}/`, {
        method: 'delete',
        headers: {
            'Authorization': `Basic ${authheader}`,
            "Content-Type": "application/json",

        },
    }).then((res) => {
        window.location.reload(true)
    });
}

function approve_follow_request(target_user) {
    let authheader = Cookies.get('authheader');
    fetch(`/followreqs/${target_user}/`, {
        method: 'post',
        headers: {
            'Authorization': `Basic ${authheader}`,
            "Content-Type": "application/json",

        },
    }).then((res) => {
        window.location.reload(true)
    });
}