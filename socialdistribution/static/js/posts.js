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
                },
                error: function(request,msg,error) {
                    console.log('fail to get lists of friend');
                }
            });  

            $(".open-visibileTo-button").click(function(){
                var visible_to_list = new Array;
                $("#myForm").show();
                $(".close-visibileTo-button").click(function(){
                    $("#myForm").hide();
                });
                $(".visibile-to-friends").change(function(){
                    var friend_url = $(this).val();
                    if ($(this).is(":checked")){
                        if (!visible_to_list.includes(friend_url)){
                            visible_to_list.push(friend_url);
                            // console.log( visible_to_list);
                        }
                    }else{
                        if (visible_to_list.includes(friend_url)){
                            var index = visible_to_list.indexOf(friend_url);
                            if (index > -1){
                                visible_to_list.splice(index, 1);
                                // console.log( visible_to_list);
                            }
                        }
                    }
                    // console.log( visible_to_list);
                    $("#id_visibleTo").val(visible_to_list.toString());
                })
            })

        }else{
            $("#id_visibleTo").val("[]");
            $(".open-visibileTo-button").css("visibility","hidden");
        }
    });


});
