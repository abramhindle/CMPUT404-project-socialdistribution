//function to show comments
//Reference: https://stackoverflow.com/questions/29321494/show-input-field-only-if-a-specific-option-is-selected/29321711
//Author: https://stackoverflow.com/users/4721273/josephus87

function displayCommentsCheck(that) {
    if (document.getElementById("showComments").style.display == "block") {
        document.getElementById("showComments").style.display = "none";
    } else {
        document.getElementById("showComments").style.display = "block";
    }
}

