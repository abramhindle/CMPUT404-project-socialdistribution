var add = "POST";
var remove = "DELETE";
$(document).ready(function() {
        $("#uploadButton").on('click', function(event) {
            document.getElementById('fileInput').click();
            event.preventDefault();
        });

        $("#closeButton").on('click', function(event) {
            $("#fileInput").replaceWith($("#fileInput").clone());
            $('#fileName').html("");
            $('#closeButton').css("visibility", "hidden");
            event.preventDefault();
        });

        $('.categoryInputFields').hide(); //Note: this is a workaround for setting the inputfields as invis to begin with

//        for api calls http://sliptree.github.io/bootstrap-tokenfield/
        $('.tagInput').on('tokenfield:createtoken', function (e) {
            var list = $(this).tokenfield('getTokensList').split(',');
            var newTag = e.attrs.value.trim();
            for (item in list) {
                if (list[item].trim() === newTag) {
                    return false;
                }
            }

            var postTagsElm = $(this).parents('.postTags');
            var postId = postTagsElm.find('.postIdHidden').val();
            //Checks whether or not we are in tag section as well as whether or not the new tag added exists in
            //the list of tags already(this is to counter this event being triggered whenever we set a token field
            //with pre-existing tags
            if (postId != undefined && postId != '' && checkIfNewlyAdded(newTag, postTagsElm)) {
                return categoryRequest(postId, newTag, add, postTagsElm);
            }

        }).on('tokenfield:removetoken', function (e) {
            var tag = e.attrs.value.trim();
            var postTagsElm = $(this).parents('.postTags');
            var postId = postTagsElm.find('.postIdHidden').val();
            if (postId != undefined && postId != '') {
                return categoryRequest(postId, tag, remove, postTagsElm)
            }
        }).tokenfield();
});

//called whenever the user has selected a file on the #uploadButton item
function onInputChanged(elm) {
    name = $(elm).val();
    if (name.length > 0) {
        $('#fileName').html(name);
        $('#closeButton').css("visibility", "visible");
    }
}

//changes the visibility of the author inputfield when posting to specific author
function changeTextFieldVisibility(value) {
    if (value === "author") {
        document.getElementById("authorTextfield").style.display = 'block';
    } else {
        document.getElementById("authorTextfield").style.display = 'none';
    }
}

//checks whether or not the new added items exists with the pre-existing tag list of a post.
//*Note* this is a workaround for event clipping of tokenfield:createToken with setTokens call
function checkIfNewlyAdded(value, categorySection) {
    var array = getCategoryInputString(categorySection.find('.tagList')).split(',');
    for (item in array) {
        if (array[item].trim() === value.trim()) {
            return false;
        }
    }
    return true;
}

//Returns a string to be rendered in the editable tokenfield obtained from list of values in the list
function getCategoryInputString(list) {
    return list.children('.tagItem').map(function(i,n) {
        var text = $.trim($(n).children('a').text());
        if (text != '' && text != undefined) {
            return text;
        }
    }).get().join(',');
}

//Changes the visibility of pretty tag list and editable tokenfield
function toggleTagEditingFields(categorySection) {
    categorySection.find('.categoryInputFields').toggle();
    categorySection.find('.tagList').toggle();
}

//changes the look of the category/tag list, be it removing an item or adding an item. This is used to
//change the lists state without refreshing the page via ajax
function modifyCategoryList(method, value, list) {
    if (method == remove) {
        list.find('.tagList').find('li').each(function() {
            if ($(this).find("a").text().trim() == value) {
                $(this).remove();
            }
        });
    } else {
        list.find('.tagList').find(' > li:nth-last-child(1)').before(
            "<li class=\"tagItem\">" +
            "<a class=\"tag glyphicon glyphicon-tag\" href=\""+value+"\"> "+value+"</a>"+
            "</li>"
        );
    }
}