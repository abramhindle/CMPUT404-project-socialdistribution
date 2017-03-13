$(function() {
    var $friend_request_button = $("#send-friend-request-button");
    var $friend_request_sent_message = $("#friend-request-sent-message");

    $friend_request_button.on('click', function () {
        var $that = $(this);
        $.post($that.data('url'), function () {
            $that.hide();
            $friend_request_sent_message.show()
        });
    });
});
