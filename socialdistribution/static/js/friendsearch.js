$(document).ready(function() {
    $('#friend-input-container > #input').keyup(function() {
        var search_text = $('#friend-input-container > #input').val();
        if (search_text !== ""){
            $.ajax({
                type: "POST",
                url: location.href,
                data: {
                    'search_text' :  search_text,
                },
                success: function(response) {
                    result = $(response).find('.friends-list');
                    $('.friends-list').html(result);
                    console.log(result);
                    
                },
                
            });
        }
        console.log(search_text);
    });

});