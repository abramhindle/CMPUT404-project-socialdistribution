$(document).ready(function() {
    // TODO: get the django friend request object,
    // If we have the friend/author api to know how 
    // many friend requests the author has
    // var requestnum = $(".post-card").attr('id')

    //TODO: this reload the page when reload the page
    // This function make the app becoem slow.
    // Need to change.
    $.ajax({
        url: location.origin + '/friends/friend_requests',
        type: 'GET', 
        success: function(data) {
            var numItems = $(".friend-list", data).length;
            $(".badge").text(numItems);
        },
    }); 

    $(".btn.send-request").click(function(){

        var author_name = $(".user_author_name").attr('id');
        var author_id = $(".user_author_id").attr('id');
        // Get the friend id
        var friend_name = $(".author-displayName").attr('id');
        var friend_id = $(".btn.send-request").attr('id');
        console.log(author_id);
        console.log(friend_id );
 
        var requestContent={
            "query":"friendrequest",
            "author": {
                "id": author_id,
                "host":location.origin,
                "displayName": author_name,
                "url":location.origin + "/author/" + author_id,
            },
            "friend": {
                "id": friend_id,
                "host":location.origin,
                "displayName":friend_name,
                "url":location.origin + "/author/" +friend_id,   
            },
        };
        console.log(requestContent );
        
        if ($(".btn.send-request").val() !== "Following"){
            $.ajax({
                url: '/api/friendrequest',
                type: 'POST',
                data: JSON.stringify(requestContent),
                success: function(result) {
                    alert("You send friend request successfully");   
                    //TODO: if I reload the page. It will become Add Friend again
                    // $(".btn.send-request").text("Following");   
                    location.replace(location.origin + '/friends/friend_following'); 
                },
                error: function(request,msg,error) {
                    alert("Invalid action"); 
                }
            }); 
        }
    });   
});