function approveUser(userID) {
    fetch('/users/approve/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authentication': AuthStore.header()
        },
        body: JSON.stringify({id: userID})
    });
}