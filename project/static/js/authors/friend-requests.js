$(function() {
    var $friend_request_button = $("#send-friend-request-button");
    var $friend_request_sent_message = $("#friend-request-sent-message");
    var $follow_button = $("#follow-button");
    var $unfollow_button = $("#unfollow-button");

    $friend_request_button.on('click', function () {
        var $that = $(this);
        $.post($that.data('url'), function () {
            $that.hide();
            $follow_button.hide();
            $friend_request_sent_message.show()
            $unfollow_button.show();
        });
    });
});
