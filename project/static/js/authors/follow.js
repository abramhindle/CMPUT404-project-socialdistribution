$(function() {
    $('#follow-button').on('click', function () {
        var $that = $(this);
        $.post($that.data('url'), function () {
            $that.hide();
        });
    });
});
