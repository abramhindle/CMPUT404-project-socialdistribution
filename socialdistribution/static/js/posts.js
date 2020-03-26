var friend_list_markup =  '<div class="form-popup" id="myForm" style="display: none;">\
  <form class="form-container">\
    <h3>Visible To</h3>\
    {{each(i) friends }}\
    <input type="radio" value="${i}">${i}</input>\
    {{/each}}\
  </form>\
</div>'

// template/posts/posts_base.html
function setImageSize() {
  var imgs = document.getElementsByClassName('imagePost');
  for (var i = 0; i < imgs.length; i++) {
    imgs[i].height = 0.8 * imgs[i].height;
    imgs[i].width = 0.8 * imgs[i].width;
  }
}

// template/posts/post_form.html
$(document).ready(function() {
    
    $(".fa-camera").hide();
    $("#id_image_file").hide();
    $('#id_contentType').on('change', function() {
        if (this.value == 'image/png;base64' || this.value == 'image/jpeg;base64') {
        $("#id_content").attr("required", false)
        $("#id_content").hide();
        $(".fa-camera").show();
        $("#id_image_file").show();
        } else {
        $(".fa-camera").hide();
        $("#id_image_file").hide();
        $("#id_content").show();
        }
    });

    /**
     * Handle delete a post
     */
    //template/posts/post_view.html
    $("#delete-post").click(function(){
        // TODO: change the url later
        // Get the post id
        var post_id = $(".post-card").attr('id')

        $.ajax({
            url: '/api/posts/' + post_id,
            method: 'DELETE',
            success: function(result) {
                alert("You deleted this post");
                //relocate to the http://<hostname>/stream
                location.replace(location.origin + '/stream');
            },
            error: function(request,msg,error) {
                alert("You don't delete this post successfully");
            }
        });

    });

    /**
     * Handle VisibleTo depend on the selection of visibility
     * 
     * VisibleTo Selection only shows when the post is not a public
     * post
     */
    $.template( "friendListTemplate", friend_list_markup );

    $("#id_visibility").change(function(){
        var authorId = $(".profile-header-info").attr("id");
        var visibility = $(this).children("option:selected").val();
        if (visibility === "PRIVATE"){
            // $(".open-visibileTo-button").append(friend_list_markup);
            $(".open-visibileTo-button").css("visibility","visible");

            $.ajax({
                url: '/api/author/'+ authorId,
                method: 'GET',
                success: function(info) {
                    console.log(info);
                    $.tmpl( "friendListTemplate", info).appendTo(".open-visibileTo-button");
                },
                error: function(request,msg,error) {
                    console.log('fail to get lists of friend');
                }
            });  

            $(".open-visibileTo-button").click(function(){
                $("#myForm").toggle();
            })

        }else{
            $(".open-visibileTo-button").css("visibility","hidden");
        }
    });

});
