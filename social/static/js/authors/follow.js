$(function() {
    var $follow_button = $("#follow-button");
    var $unfollow_button = $("#unfollow-button");

    $follow_button.on('click', function () {
        var $that = $(this);
        $.post($that.data('url'), function () {
            $that.hide();
            $unfollow_button.show()
        });
    });

    $unfollow_button.on('click', function () {
        var $that = $(this);
        $.post($that.data('url'), function () {
            $that.hide();
            $follow_button.show()
        });
    });
});
